from datetime import datetime as dt
from pyscript import document
from pyweb import pydom

tasks = []

#Definindo a página de seleção para trabalhar com o documento.
def q(selector, root=document):
    return root.querySelector(selector)

#Seleção do objeto DOM HTML para trabalhar com ele.
task_template = pydom.Element(q("#task-template").content.querySelector(".task"))

#Criação da dos "Arrays de HTML" que irão estar lidando no Front com a adição de Tarefas
task_list = pydom["#list-tasks-container"][0]
new_task_content = pydom["#new-task-content"][0]
new_task_priority = pydom["#new-task-priority"][0]


def add_task(e):
    # Tratamento de Tarefa Vazia
    if not new_task_content.value:
        return None
    
    #Tratamento do tipo de prioridade que a Tarefa irá atribuir
    priority = ""
    if(new_task_priority.value == "task-priority-high"):
        priority = "Alta"
    elif(new_task_priority.value == "task-priority-medium"):
        priority = "Média"
    else:
        priority = "Baixa"
        
        
    # Formatação de Data
    dateTimeFormat = f"{dt.now().day}/{dt.now().month}/{dt.now().year}"
    
    # Criação do OBJETO Tarefa
    task_id = f"task-{len(tasks)}"
    task = {
        "id": task_id,
        "priority": priority,
        "content": new_task_content.value,
        "done": False,
        "created_at": dateTimeFormat,
    }

    tasks.append(task)

  #Adiciona o elemento task à página como um novo nó na lista clonando de um template
    task_html = task_template.clone()
    task_html.id = task_id

    #Adicionado as variáveis inputadas para o template
    task_html_check = task_html.find("input")[0]
    task_html_title = task_html.find(".task-title")[0]
    task_html_priority = task_html.find(".task-priority")[0]
    task_html_createdAt = task_html.find(".task-createdAt")[0]
    #Adicionando uma classe para estilizar com CSS
    task_html_priority.add_class(new_task_priority.value)
    
    
    task_html_title._js.textContent = task["content"]
    task_html_priority._js.textContent = task["priority"]
    task_html_createdAt._js.textContent = task["created_at"]
    task_list.append(task_html)
    
    #Checagem da Tarefa se já foi concluída e atribuindo CSS.

    def check_task(evt=None):
        task["done"] = not task["done"]
        task_html_title._js.classList.toggle("line-through", task["done"])

    new_task_content.value = ""
    task_html_check._js.onclick = check_task


def add_task_event(e):
    if e.key == "Enter":
        add_task(e)


new_task_content.onkeypress = add_task_event
