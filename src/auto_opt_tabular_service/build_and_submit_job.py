from fastapi import APIRouter, Header
from pydantic import BaseModel
from tapipy.tapis import Tapis

# creating router
router = APIRouter()

# defining run_job model
class Job(BaseModel):
	name: str
	exec_system_id: str
	cores_per_node: int
	memory_mb: int
	max_minutes: int
	billing_account: str
	ds_path_name: str
	ds_path_source_url: str
	ds_path: str
	task_type: str = "reg"
	split_func: str = "split_20"
	eval_type: str = "avg_bag"
	gen_strat: str = "best"
	metric: str = "mae + rmse - r2"
	err_path: str
	params_path: str
	bags: int = 3
	eval_iterations: int = 3
	


@router.post("/run_job")
async def run_job(job:Job, x_token:str=Header(...)):
	# ensuring input type
	if not isinstance(job, Job):
		raise TypeError(f"🛑 unexpected type {type(job)}")
	if not isinstance(job.exec_system_id, str):
		raise TypeError(f"🛑 unexpected type {type(job.exec_system_id)}")
	if not isinstance(job.ds_path_name, str):
		raise TypeError(f"🛑 unexpected type {type(job.ds_path_name)}")
	if not isinstance(job.ds_path_source_url, str):
		raise TypeError(f"🛑 unexpected type {type(job.ds_path_source_url)}")
	if not isinstance(job.ds_path, str):
		raise TypeError(f"🛑 unexpected type {type(job.ds_path)}")
	if not isinstance(job.metric, str):
		raise TypeError(f"🛑 unexpected type {type(job.metric)}")
	if not isinstance(job.err_path, str):
		raise TypeError(f"🛑 unexpected type {type(job.err_path)}")
	if not isinstance(job.params_path, str):
		raise TypeError(f"🛑 unexpected type {type(job.params_path)}")
	if not isinstance(job.bags, int):
		raise TypeError(f"🛑 unexpected type {type(job.bags)}")
	if not isinstance(job.eval_iterations, int):
		raise TypeError(f"🛑 unexpected type {type(job.eval_iterations)}")
	if not isinstance(job.max_minutes, int):
		raise TypeError(f"🛑 unexpected type {type(job.max_minutes)}")
	if not isinstance(job.billing_account, str):
		raise TypeError(f"🛑 unexpected type {type(job.billing_account)}")
	# ensuring input parameter types
	if job.task_type != "reg" and job.task_type != "class":
		raise ValueError(f"🛑 unexpected value {job.task_type}")
	# creating list of potential split functions
	pot_split_funcs = ["split_15","split_20","split_30","split_index_15","split_index_20","split_index_30"]
	if job.split_func not in pot_split_funcs:
		raise ValueError(f"🛑 unexpected value {job.split_func}")
	# ensuing input parameter eval_type
	if job.eval_type != "avg" and job.eval_type != "bag" and job.eval_type != "avg_bag":
		raise ValueError(f"🛑 unexpected value {job.eval_type}")
	# ensuring input parameter gen_strat
	if job.gen_strat != "best" and job.gen_strat != "mean":
		raise ValueError(f"🛑 unexpected value {job.gen_strat}")
	# building out job dict
	job_dict = {
		"name":job.name,
		"appId":"auto-opt-tabular-service-app",
		"execSystemId":job.exec_system_id,
		"appVersion":"0.1",
		"jobType":"BATCH",
		"nodeCount":1,
		"coresPerNode":1,
		"memoryMB":job.memory_mb,
		"maxMinutes":job.max_minutes,
		"parameterSet": {
			"schedulerOptions":[
				{"name":"TACC_ACCT", "arg": f"--account={job.billing_account}"},
				{"name":"cpus_per_task", "arg": f"--cpus-per-task={job.cores_per_node}"}
			],
			"appArgs":[
				{"arg": f"--ds_path={job.ds_path}"},
				{"arg": f"--task_type={job.task_type}"},
				{"arg": f"--split_func={job.split_func}"},
				{"arg": f"--eval_iterations={job.eval_iterations}"},
				{"arg": f"--bags={job.bags}"},
				{"arg": f"--eval_type={job.eval_type}"},
				{"arg": f"--gen_strat={job.gen_strat}"},
				{"arg": f"--metric={job.metric}"},
				{"arg": f"--err_path={job.err_path}"},
				{"arg": f"--params_path={job.params_path}"}
			]
		},
		"fileInputs": [
			{
				"name":job.ds_path_name,
				"sourceUrl":job.ds_path_source_url,
				"targetPath":job.ds_path
			}
		]
	}
	# creating tapis object
	t = Tapis(base_url="https://tacc.tapis.io", jwt=x_token)
	# submitting job
	res = t.jobs.submitJob(**job_dict)
	# retunring tapis job unique identifier
	return res.uuid
