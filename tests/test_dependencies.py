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
            assert streamlit is not None
        except ImportError:
            pytest.skip("streamlit not installed")
    
    @pytest.mark.unit
    def test_pandas_import(self):
        """Test that pandas can be imported"""
        try:
            import pandas
            assert pandas is not None
        except ImportError:
            pytest.skip("pandas not installed")
    
    @pytest.mark.unit
    def test_openai_import(self):
        """Test that openai can be imported"""
        try:
            import openai
            assert openai is not None
        except ImportError:
            pytest.skip("openai not installed")
    
    @pytest.mark.unit
    def test_beautifulsoup_import(self):
        """Test that beautifulsoup4 can be imported"""
        try:
            from bs4 import BeautifulSoup
            assert BeautifulSoup is not None
        except ImportError:
            pytest.skip("beautifulsoup4 not installed")
    
    @pytest.mark.unit
    def test_lxml_import(self):
        """Test that lxml can be imported"""
        try:
            import lxml
            assert lxml is not None
        except ImportError:
            pytest.skip("lxml not installed")
    
    @pytest.mark.unit
    def test_docx_import(self):
        """Test that python-docx can be imported"""
        try:
            from docx import Document
            assert Document is not None
        except ImportError:
            pytest.skip("python-docx not installed")
    
    @pytest.mark.unit
    def test_langchain_imports(self):
        """Test that langchain packages can be imported"""
        try:
            from langchain.llms import OpenAI
            from langchain.chat_models import ChatOpenAI
            from langchain.embeddings.openai import OpenAIEmbeddings
            assert OpenAI is not None
            assert ChatOpenAI is not None
            assert OpenAIEmbeddings is not None
        except ImportError:
            pytest.skip("langchain packages not installed")
    
    @pytest.mark.unit
    def test_weasyprint_import(self):
        """Test that weasyprint can be imported"""
        try:
            import weasyprint
            assert weasyprint is not None
        except ImportError:
            pytest.skip("weasyprint not installed")
    
    @pytest.mark.unit
    def test_markdown_pdf_import(self):
        """Test that markdown-pdf can be imported"""
        try:
            from markdown_pdf import MarkdownPdf
            assert MarkdownPdf is not None
        except ImportError:
            pytest.skip("markdown-pdf not installed")
