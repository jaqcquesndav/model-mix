"""
Test script to verify Langchain imports are working correctly.
This test validates that all required Langchain components can be imported.
"""

def test_langchain_imports():
    """Test that all Langchain imports work correctly."""
    try:
        # Test langchain_openai imports
        from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings
        print("✓ Successfully imported: OpenAI, ChatOpenAI, OpenAIEmbeddings from langchain_openai")
        
        # Test langchain_community imports
        from langchain_community.document_loaders import PyPDFLoader
        from langchain_community.vectorstores import FAISS
        print("✓ Successfully imported: PyPDFLoader, FAISS from langchain_community")
        
        # Test core langchain imports
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.chains import ConversationalRetrievalChain
        from langchain.memory import ConversationBufferMemory
        print("✓ Successfully imported: RecursiveCharacterTextSplitter, ConversationalRetrievalChain, ConversationBufferMemory from langchain")
        
        print("\n✅ All Langchain imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\nPlease ensure all dependencies are installed:")
        print("  pip install langchain>=0.1.0 langchain-community>=0.0.20 langchain-openai>=0.0.5")
        return False

if __name__ == "__main__":
    success = test_langchain_imports()
    exit(0 if success else 1)
