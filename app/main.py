from fastapi import FastAPI, HTTPException

from langchain.messages import AIMessage, HumanMessage

from app.agent.graph import run_agent
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(
    title='Agentic Chatbot API',
    description='FastAPI backend for a LangGraph tool-using agent.',
    version='1.0.0',
)


@app.get('/')
def root():
    return {
        'message': 'Agentic Chatbot API is running.',
        'docs': '/docs',
        'health': '/health',
    }


@app.get('/health')
def health():
    return {'status': 'ok'}


def _to_langchain_messages(history):
    messages = []
    for item in history:
        if item.role == 'user':
            messages.append(HumanMessage(content=item.content))
        else:
            messages.append(AIMessage(content=item.content))
    return messages


@app.post('/chat', response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        messages = _to_langchain_messages(request.history)
        messages.append(HumanMessage(content=request.message))

        result = run_agent(messages)
        final_message = result['messages'][-1]
        answer = str(getattr(final_message, 'content', ''))

        tool_calls = []
        for message in result['messages']:
            for tool_call in (getattr(message, 'tool_calls', None) or []):
                name = tool_call.get('name')
                if name:
                    tool_calls.append(name)

        return ChatResponse(answer=answer, tool_calls=tool_calls)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc