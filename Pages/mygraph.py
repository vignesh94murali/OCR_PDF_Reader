from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os, re
# from Pages.utility import docExtract2,chunk_text,summarize_with_llm,summarize_batches,comparison_tool
from dotenv import load_dotenv
from langgraph.graph import START, StateGraph, MessagesState
# from langgraph.graph.graph import set_config
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
# from IPython.display import Image, display
from typing import List
import httpx
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGGRAPH__RECURSION_LIMIT"] = "50"

groqapi_key = os.getenv("GROQ_API_KEY")
chat_model = os.getenv("CHAT_MODEL")
http_client = httpx.Client(verify=False)


def docExtract2(file_path):
    if file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
        data = loader.load()
        return data
    elif file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        data = loader.load()
        return data
    else:
        return "File not in .docx/.pdf format"


def chunk_text(text):
    text_splitter = RecursiveCharacterTextSplitter(

        chunk_size=200,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", '\n \n']
    )
    texts = text_splitter.split_documents(text)
    text = []
    for t in texts:
        text.append(t.page_content)
    # print(texts[0])
    # print(texts[1])
    return text


def summarize_with_llm(text):
    """Summarizes the text given.
      Args:
            text:text chunk provided

    """
    prompt = (
        "You are an advanced AI language model trained for text summarization and you have deep understanding of legal documents and it's nuances."
        "Given the following input text, generate a concise, coherent, and accurate summary while preserving the key insights and main ideas."
        "Ensure that the summary maintains the original context, removes redundancy, and enhances readability."
        "If the text is technical or domain-specific, retain the essential terminology while simplifying complex explanations."
        "Output the summary in a structured format if applicable (e.g., bullet points for key takeaways or paragraphs for narrative coherence)."
        "Directly write summary content without adding any extra sentences in beginning and do not add 'Here is a concise and accurate summary of the input text in a structured format:' or similar text in beginning"
        f"Text:\n{text}\n\n"
        )

    system = "You are an advanced AI language model trained for text summarization and you have deep understanding of legal documents and it's nuances."

    final_prompt = ChatPromptTemplate.from_messages([("system", system), ("human", prompt)])
    llm = ChatGroq(groq_api_key=groqapi_key, model=chat_model, http_client=http_client)
    chain = final_prompt | llm
    response = chain.invoke({'Text': text})
    output = response.content
    return {'summary': output}


def summarize_batches(file_path: str, batch_size: int = 10) -> List[str]:
    """extracts data from the file given in parameter, creates chunks from extracted data,Summarize chunks in batches using LLM.
    Args:
        file_path: file name
        batch_size: number of chunks to be summarized in a batch
    """

    text = docExtract2(file_path)
    chunks = chunk_text(text)
    summaries = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        combined_text = " ".join(batch)
        summary = summarize_with_llm(combined_text)

        summaries.append(summary['summary'])
    return summaries


def comparison_tool(summary1: List[str], summary2: List[str]) -> dict:

    """Executed only for doing comparison, takes lists of summary of documents and performs comparison using LLM.

    Args:
        summary1: list of summary of first document
        summary2: list of summary of second document
    """
    # prompt = (
    #     "You are an advanced AI language model trained for text summarization and understanding legal documents and it's nuances."
    #     "Given the set of two lists having summary generated from two different documents,your task is to generate a concise, coherent, and accurate comparison while preserving the key insights and main ideas."
    #     "Ensure that the comparison maintains the original context, removes redundancy, and enhances readability. If the text is technical or domain-specific, retain the essential terminology while simplifying complex explanations."
    #     "Output the comparison in a structured format e.g., bullet points for key takeaways or paragraphs for narrative coherence."
    #     f"Summary1:\n{summary1}\n\n"
    #     f"Summary2:\n{summary2}\n\n"
    #     )

    human_prompt = (
        "Given the following two sets of summaries from two different legal documents, generate a concise and structured comparison.\n\n"
        "Summary1:\n{summary1}\n\n"
        "Summary2:\n{summary2}\n\n"
        "Provide the comparison in bullet points or structured format."
    )

    system = "You are an advanced AI language model trained for comparing legal document summaries."

    # final_prompt = ChatPromptTemplate.from_messages([("system", system), ("human", prompt)])
    
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", human_prompt)
    ])

    llm = ChatGroq(groq_api_key=groqapi_key, model=chat_model, http_client=http_client)
    
    chain = final_prompt | llm
    
    # response = chain.invoke({'Summary1': summary1, 'summary2': summary2})
    response = chain.invoke({
        "summary1": "\n".join(summary1),
        "summary2": "\n".join(summary2)
    })
    
    output = response.content
    
    return {'comparison': output}


# System message
sys_msg = SystemMessage(
    content="You are a helpful AI assistant designed to answer general queries and analyze uploaded files."
            "For general questions, provide direct responses **without using any tools**."
            "If a query requires processing files (such as summarization, content extraction, or comparison), **only then** use the appropriate tools."
            "Before using tools, carefully analyze whether they are truly necessary. If answering without tools is possible, do so."

            "Guidelines:"
            "1. If a query can be answered directly, respond without tools."
            "2. If the user uploads one file and asks for insights, summarize or extract relevant details."
            "3. If the user uploads multiple files and asks for comparison, use comparison tools."
            "4. Never use tools unless processing files or performing a task that requires them."

    )


# def assistant(state: MessagesState):
#     return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

def assistant(state: MessagesState):
    # Use a non-tool LLM to get next message
    result = llm.invoke([sys_msg] + state["messages"])
    return {"messages": [result]}



tools = [summarize_batches, comparison_tool]
llm = ChatGroq(groq_api_key=groqapi_key, model=chat_model, http_client=http_client)
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)


def createGraph():
    # Graph
    builder = StateGraph(MessagesState)
    # Define nodes: these do the work
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    # Define edges: these determine how the control flow moves
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
        # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    react_graph = builder.compile()
    return react_graph

