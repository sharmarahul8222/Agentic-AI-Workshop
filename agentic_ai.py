from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent

import subprocess #subprocess is a package that can run command on your terminal

SYSTEM_PROMPT = """
You are a Docker Expert. You can explain things in 1-2 lines max.
You don't overthink, hallucinate or keep reasoning in a loop
You Reason and Act accordingly to user prompt.

These are the things you do:
1. You tell about errors (What went wrong, etc)
2. You tell about the root cause (What was the cause likely)
3. You tell about the fix or solution in short
"""

@tool
def show_running_containers():
   """ Tool 1: Show running containers """    # docstring 
   result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
   return result.stdout

@tool
def list_containers():
   """ Tool 1: Show all containers running and stopped"""    # docstring 
   result = subprocess.run(["docker", "ps", "-a"], capture_output=True, text=True)
   return result.stdout

@tool
def show_container_logs_by_name(container_name):
   """ Tool 2: Show logs for a specific container """       # docstring 
   result = subprocess.run(["docker", "logs", container_name], capture_output=True, text=True)
   return result.stdout

@tool
def inspect_container(container_name):
   """ Tool 4: Get detailed info about a Docker container (state, config, network). """       # docstring 
   result = subprocess.run(["docker", "inspect", container_name], capture_output=True, text=True)
   return result.stdout

@tool
def list_pods(namespace: str = "default"):
    """List all pods in a Kubernetes namespace with their status."""        # docstring
    result = subprocess.run(["kubectl", "get", "pods", "-n", namespace], capture_output=True, text=True)
    return result.stdout

@tool
def describe_pod(pod_name: str, namespace: str = "default"):
    """Get detailed info about a Kubernetes pod including events and conditions."""         # docstring
    result = subprocess.run(["kubectl", "describe", "pod", pod_name, "-n", namespace], capture_output=True, text=True)
    return result.stdout

@tool
def get_events(namespace: str = "default"):
    """Get recent Kubernetes events in a namespace (useful for troubleshooting)."""         # docstring
    result = subprocess.run(["kubectl", "get", "events", "-n", namespace, "--sort-by=.lastTimestamp"], capture_output=True, text=True)
    return result.stdout


llm = ChatOllama(model="gemma4", temperature="0.8", system=SYSTEM_PROMPT)
tools = [show_running_containers, list_containers, show_container_logs_by_name, inspect_container, list_pods, describe_pod, get_events]

agent = create_agent(llm, tools)


while True:
   user_input = input("Enter your message:\n")

   if user_input == "exit":
       break
   response = agent.invoke({
       "messages": [{
           "role": "user",
           "content": user_input,
           }]})

   print(response["messages"][-1].content)

