# RAG 应用开发实战

## 1. 什么是 RAG

RAG（Retrieval-Augmented Generation，检索增强生成）是一种结合检索系统和生成模型的技术：

- **检索**：从知识库中找到相关内容
- **增强**：将检索结果加入 prompt
- **生成**：基于增强的上下文生成答案

```
用户问题 → 检索系统 → 相关文档 → LLM → 最终答案
```

## 2. RAG 核心组件

```python
"""
RAG 系统架构
"""

#                    ┌─────────────────┐
#                    │   文档数据源     │
#                    │  (PDF, 网页等)   │
#                    └────────┬────────┘
#                             │
#                    ┌────────▼────────┐
#                    │   文档加载器     │
#                    │   DocumentLoader │
#                    └────────┬────────┘
#                             │
#                    ┌────────▼────────┐
#                    │    文本分割      │
#                    │  TextSplitter   │
#                    └────────┬────────┘
#                             │
#                    ┌────────▼────────┐
#                    │   向量化模型     │
#                    │  Embedding     │
#                    └────────┬────────┘
#                             │
#                    ┌────────▼────────┐
#                    │    向量数据库    │
#                    │  VectorStore   │
#                    └────────┬────────┘
#                             │
#                    ┌────────▼────────┐
#                    │    检索系统     │
#                    │   Retrieval    │
#                    └────────┬────────┘
#                             │
#                    ┌────────▼────────┐
#                    │     LLM 生成    │
#                    │   Generation   │
#                    └─────────────────┘
```

## 3. 完整实现

### 3.1 环境配置

```bash
pip install langchain langchain-community langchain-openai \
    chromadb pypdf unstructured sentence-transformers
```

### 3.2 文档加载与处理

```python
from langchain_community.document_loaders import PyPDFLoader, WebLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 加载 PDF
loader = PyPDFLoader("document.pdf")
pages = loader.load()

# 加载网页
loader = WebLoader("https://example.com/article")
web_docs = loader.load()

# 合并所有文档
all_docs = pages + web_docs

# 文本分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = text_splitter.split_documents(all_docs)
print(f"生成了 {len(chunks)} 个文本块")
```

### 3.3 向量化与存储

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 初始化 embedding 模型
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# 创建向量数据库
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 保存到磁盘
vectorstore.persist()
```

### 3.4 检索系统

```python
from langchain.retrievers import BM25Retriever
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.document_compressors import LLMChainExtractor

# 基础检索
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# 语义搜索示例
query = "Python 异步编程"
results = retriever.get_relevant_documents(query)

for i, doc in enumerate(results):
    print(f"结果 {i+1}: {doc.page_content[:100]}...")
    print(f"来源: {doc.metadata}")
```

### 3.5 带历史的对话

```python
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# 初始化 LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# 对话记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 创建对话检索链
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": chat_prompt}
)

# 问答
question = "Python 异步编程有什么优势？"
result = qa_chain({"question": question})
print(result["answer"])
```

## 4. 完整 RAG 应用示例

```python
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

class RAGApplication:
    def __init__(self, persist_dir="./vector_db"):
        self.persist_dir = persist_dir
        
        # 配置 API Key
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        
        # 初始化组件
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
        
        # 加载向量数据库
        self.vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=self.embeddings
        )
        
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 5}
        )
        
        # 自定义提示词
        self.prompt = PromptTemplate(
            template="""基于以下上下文回答问题。如果上下文中没有相关信息，请说明你不知道。

上下文:
{context}

问题: {question}

回答:""",
            input_variables=["context", "question"]
        )
        
        # 创建 QA 链
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
    
    def ask(self, question: str) -> dict:
        """问答"""
        result = self.qa_chain({"query": question})
        
        return {
            "answer": result["result"],
            "sources": [
                {
                    "content": doc.page_content[:200],
                    "source": doc.metadata.get("source", "Unknown")
                }
                for doc in result["source_documents"]
            ]
        }
    
    def add_documents(self, documents):
        """添加文档"""
        self.vectorstore.add_documents(documents)
        self.vectorstore.persist()

# 使用示例
if __name__ == "__main__":
    rag = RAGApplication()
    
    # 问答
    result = rag.ask("Python 3.12 有哪些新特性？")
    print(f"答案: {result['answer']}")
    print(f"来源文档: {len(result['sources'])} 个")
```

## 5. 高级技巧

### 5.1 混合检索

```python
from langchain.retrievers import EnsembleRetriever

# BM25 检索器
bm25_retriever = BM25Retriever.from_texts(texts)
bm25_retriever.k = 5

# 语义检索器
vectorstore_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

# 组合检索 (权重平均)
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vectorstore_retriever],
    weights=[0.3, 0.7]
)
```

### 5.2 重排序

```python
from langchain_community.cross_encoders import CohereCrossEncoder

# 重排序模型
cross_encoder = CohereCrossEncoder(model="rerank-english-v2.0")

def rerank_documents(query, documents, top_n=5):
    """对检索结果重排序"""
    doc_pairs = [(query, doc.page_content) for doc in documents]
    scores = cross_encoder.predict(doc_pairs)
    
    # 按分数排序
    ranked_indices = sorted(range(len(scores)), 
                          key=lambda i: scores[i], 
                          reverse=True)
    
    return [documents[i] for i in ranked_indices[:top_n]]
```

### 5.3 查询扩展

```python
from langchain.prompts import PromptTemplate

EXPANSION_PROMPT = PromptTemplate(
    template="""为一个问题生成3个不同的表述方式，以便更好地检索相关文档。

问题: {question}

表述1:
表述2:
表述3:""",
    input_variables=["question"]
)

def expand_query(question: str) -> list:
    """查询扩展"""
    response = llm.invoke(EXPANSION_PROMPT.format(question=question))
    queries = [question] + response.content.split('\n')[1:4]
    return [q.strip() for q in queries if q.strip()]

# 使用扩展查询
queries = expand_query("Python async")
all_results = []
for q in queries:
    results = retriever.get_relevant_documents(q)
    all_results.extend(results)
```

## 6. 性能优化

### 6.1 缓存 embedding

```python
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

# 本地缓存
store = LocalFileStore("./cache/embeddings")

cached_embedder = CacheBackedEmbeddings(
    underlying_embeddings=embeddings,
    document_embedding_cache=store
)
```

### 6.2 批量处理

```python
# 批量添加文档
from tqdm import tqdm

def batch_add_documents(vectorstore, documents, batch_size=100):
    """批量添加文档"""
    for i in tqdm(range(0, len(documents), batch_size)):
        batch = documents[i:i + batch_size]
        vectorstore.add_documents(batch)
    vectorstore.persist()
```

## 7. 评估指标

```python
from langchain.evaluation import load_evaluator

# 准确性评估
evaluator = load_evaluator("contextual_precision")

def evaluate_rag(question: str, answer: str, contexts: list):
    """评估 RAG 输出质量"""
    results = evaluator.evaluate_strings(
        prediction=answer,
        reference=question,
        input=contexts
    )
    return results
```

## 8. 下一步学习

- [模型部署 Ollama](./04-模型部署/01-本地部署Ollama.md)
- [向量数据库详解](../05-向量数据库/01-向量数据库对比.md)
