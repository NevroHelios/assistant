from typing import List, Dict, Any
from ollama import AsyncClient
import logging
from typing import List, AsyncGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class LocalRAGPipeline:
    def __init__(self, model_name: str = "llama3.1:latest", host: str = "http://localhost:11434", retriever=None):
        self.model_name = model_name
        self.client = AsyncClient(host=host)
        self.retriever = retriever  # AsyncRetriever will be set here

    async def set_retriever(self, retriever):
        """Set the retriever for the RAG system."""
        self.retriever = retriever

    async def retrieve(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant documents."""
        if self.retriever is None:
            logging.warning("Retriever not set. Running without context.")
            return [{"content": {"content": ""}}]
        return await self.retriever.retrieve(query)

    async def generate(self, prompt: str, context: List[str]) -> AsyncGenerator[str, None]:
        """Generate a response using the local LLaMA model."""
        full_prompt = f"Context:\n{' '.join(context)}\n\nQuestion: {prompt}\n\nAnswer:"
        if not context:
            full_prompt = f"Question: {prompt}\n\nAnswer:"
            
        try:
            response = await self.client.generate(model=self.model_name, prompt=full_prompt)
            full_responce = response['response']

            for chunk in self.chunk_response(full_responce):
                yield chunk

        except Exception as e:
            logging.error(e)
            yield f"Error: {e}"
        
    def chunk_response(self, response: str, chunk_size: int = 50):
        """Chunk the response into smaller chunks."""
        for i in range(0, len(response), chunk_size):
            yield response[i:i+chunk_size]
            
            
    async def run(self, query: str):
        """Run the full RAG pipeline."""
        retrieved_docs = await self.retrieve(query)
        context = [doc['content']['content'] for doc in retrieved_docs if isinstance(doc['content'], dict)]
        # return await self.generate(query, context)
        
        async for chunk in self.generate(query, context):
            yield chunk
            
            
            

async def main():
    pipeline = LocalRAGPipeline()
    async for response in pipeline.run("i thiunk genshin impact is the best! change my mind."):
        print(response)

            
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())