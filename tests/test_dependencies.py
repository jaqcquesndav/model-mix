"""
Tests to verify that all required dependencies are properly installed
"""
import pytest


class TestDependencies:
    """Tests for verifying dependencies are installed"""
    
    @pytest.mark.unit
    def test_streamlit_import(self):
        """Test that streamlit can be imported"""
        try:
            import streamlit
            assert True
        except ImportError:
            pytest.fail("streamlit could not be imported")
    
    @pytest.mark.unit
    def test_pandas_import(self):
        """Test that pandas can be imported"""
        try:
            import pandas
            assert True
        except ImportError:
            pytest.fail("pandas could not be imported")
    
    @pytest.mark.unit
    def test_openai_import(self):
        """Test that openai can be imported"""
        try:
            import openai
            assert True
        except ImportError:
            pytest.fail("openai could not be imported")
    
    @pytest.mark.unit
    def test_beautifulsoup_import(self):
        """Test that beautifulsoup4 can be imported"""
        try:
            from bs4 import BeautifulSoup
            assert True
        except ImportError:
            pytest.fail("beautifulsoup4 could not be imported")
    
    @pytest.mark.unit
    def test_lxml_import(self):
        """Test that lxml can be imported"""
        try:
            import lxml
            assert True
        except ImportError:
            pytest.fail("lxml could not be imported")
    
    @pytest.mark.unit
    def test_docx_import(self):
        """Test that python-docx can be imported"""
        try:
            from docx import Document
            assert True
        except ImportError:
            pytest.fail("python-docx could not be imported")
    
    @pytest.mark.unit
    def test_langchain_imports(self):
        """Test that langchain packages can be imported"""
        try:
            from langchain.llms import OpenAI
            from langchain.chat_models import ChatOpenAI
            from langchain.embeddings.openai import OpenAIEmbeddings
            assert True
        except ImportError as e:
            pytest.fail(f"langchain packages could not be imported: {e}")
    
    @pytest.mark.unit
    def test_weasyprint_import(self):
        """Test that weasyprint can be imported"""
        try:
            import weasyprint
            assert True
        except ImportError:
            pytest.fail("weasyprint could not be imported")
    
    @pytest.mark.unit
    def test_markdown_pdf_import(self):
        """Test that markdown-pdf can be imported"""
        try:
            from markdown_pdf import MarkdownPdf
            assert True
        except ImportError:
            pytest.fail("markdown-pdf could not be imported")
