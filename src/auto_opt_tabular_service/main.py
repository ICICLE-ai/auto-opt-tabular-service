from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auto_opt_tabular_service.health import router as health_router
from auto_opt_tabular_service.build_and_submit_job import router as job_router
from auto_opt_tabular_service.config import get_settings

app = FastAPI(title=get_settings().service_name)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)
app.include_router(health_router)
app.include_router(job_router)
