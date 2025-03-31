from locust import HttpUser, task, between, events
import random
import uuid
import time
import psutil
import logging
from faker import Faker

fake = Faker()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalCaseAnalyzeUser(HttpUser):
    wait_time = between(0.5, 2)  # More aggressive wait times for load testing
    
    @task(3)
    def generate_report(self):
        case_name = f"Case-{uuid.uuid4()}"
        case_text = fake.paragraph(nb_sentences=random.randint(5, 20))  # Varied text length
        
        payload = {
            "case_name": case_name,
            "case_text": case_text,
            "messages": [
                {"role": "user", "content": "Analyze this case thoroughly"}
            ]
        }
        
        start_time = time.time()
        response = self.client.post("/api/generate-report", json=payload)
        elapsed_time = time.time() - start_time
        
        logger.info(f"Report generation - Response time: {elapsed_time:.2f}s, Status: {response.status_code}")
        
        # Track memory usage
        memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        logger.info(f"Memory usage after report generation: {memory_usage:.2f}MB")
    
    @task(7)
    def chat_with_report(self):
        report_id = f"Case-{random.randint(1, 100)}"
        messages = [
            {"role": "user", "content": fake.sentence()},
            {"role": "assistant", "content": fake.sentence()},
            {"role": "user", "content": fake.paragraph(nb_sentences=random.randint(1, 5))}  # More varied messages
        ]
        
        payload = {
            "report_id": report_id,
            "messages": messages
        }
        
        start_time = time.time()
        response = self.client.post("/api/chat", json=payload)
        elapsed_time = time.time() - start_time
        
        logger.info(f"Chat response - Response time: {elapsed_time:.2f}s, Status: {response.status_code}")
        
        # Track memory usage
        memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        logger.info(f"Memory usage after chat: {memory_usage:.2f}MB")
    
    @task(1)
    def deprecated_endpoint(self):
        start_time = time.time()
        response = self.client.post("/copilotkit/")
        elapsed_time = time.time() - start_time
        
        logger.info(f"Deprecated endpoint - Response time: {elapsed_time:.2f}s, Status: {response.status_code}")

    @task(2)
    def mixed_workflow(self):
        """Test complete workflow: generate report then chat about it"""
        # Generate report
        case_name = f"Case-{uuid.uuid4()}"
        case_text = fake.paragraph(nb_sentences=random.randint(5, 15))
        
        report_payload = {
            "case_name": case_name,
            "case_text": case_text,
            "messages": [{"role": "user", "content": "Analyze this case"}]
        }
        
        report_response = self.client.post("/api/generate-report", json=report_payload)
        report_id = report_response.json().get("report_id")
        
        if report_id:
            # Chat about the report
            chat_payload = {
                "report_id": report_id,
                "messages": [
                    {"role": "user", "content": "What are the key points?"},
                    {"role": "assistant", "content": "Here's my analysis..."},
                    {"role": "user", "content": "Can you summarize the main arguments?"}
                ]
            }
            self.client.post("/api/chat", json=chat_payload)

if __name__ == "__main__":
    import os
    os.system("locust -f load_test.py --headless -u 100 -r 10 --run-time 5m")  # Default to headless mode with 100 users
