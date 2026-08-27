import asyncio
import time
import itertools
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_pinecone import PineconeVectorStore
from app.ai.embeddings import get_embedding_function
from app.config import settings

embedding_function=get_embedding_function()

vectorStore= PineconeVectorStore(
        index_name="travel-info",
        embedding=embedding_function,
        pinecone_api_key=settings.PINECONE_API,
        namespace="aaa"
    )   

async def webscrapper():

#     config = CrawlerRunConfig(
#     # Content thresholds
#     word_count_threshold=10,        # Minimum words per block

#     # Tag exclusions
#     excluded_tags=['form', 'header', 'footer', 'nav'],

#     # Link filtering
#     exclude_external_links=True,    
#     exclude_social_media_links=True,
#     # Block entire domains
#     exclude_domains=["adtrackers.com", "spammynews.org"],    
#     exclude_social_media_domains=["facebook.com", "twitter.com"],

#     # Media filtering
#     exclude_external_images=True
# )

#     async with AsyncWebCrawler() as crawler:
#         result = await crawler.arun(
#             "https://indonesia.tripcanvas.co/bali/budget-travel-bali/",config=config
#         )
#         # print(result.markdown)
#         print("----------------------------------------")
#         list_of_links=result.links["internal"]
    
#         link_list=[link["href"]for link in list_of_links]
#         for link in link_list:
#             print(link)
        
#-----------------deep crawling-----------------
    
    browser_config = BrowserConfig(
        headless=True,
        enable_stealth=True,        # Modifies navigator.webdriver and browser fingerprints
        
    )

    # Configure a 2-level deep crawl
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2, 
            include_external=False,
            max_pages=10,
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True,
        word_count_threshold=10,        # Minimum words per block

    # Tag exclusions
    excluded_tags=['form', 'header', 'footer', 'nav'],

    # Link filtering
    exclude_external_links=True,    
    exclude_social_media_links=True,
    # Block entire domains
    exclude_domains=["adtrackers.com", "spammynews.org"],    
    exclude_social_media_domains=["facebook.com", "twitter.com"],

    # Media filtering
    exclude_external_images=True,
    delay_before_return_html=2.5, # Gives Cloudflare's JS time to execute & resolve
        magic=True,                   # Handles consent popups & anti-bot fallbacks automatically
        wait_until="domcontentloaded",
        page_timeout=30000              # <--- Reduces wait timeout from 60s to 30s so failures happen faster
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun("https://www.aaa.com/tripcanvas/category/destinations", config=config)

        print(f"Crawled {len(results)} pages in total")
        documents=[]
        # Access individual results
        for result in results: 
            print("===========================================") # Show first 3 results
            print(f"URL: {result.url}")
            print(f"Depth: {result.metadata.get('depth', 0)}")
            print("===========================================")
            headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]

            markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
            md_header_splits = markdown_splitter.split_text(result.markdown)
            chunk_size = 1000
            chunk_overlap = 50
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )

            # Split
            splits = text_splitter.split_documents(md_header_splits)
            documents.append(splits)
            print(f"Number of chunks:{len(splits)}")
    merged_docs=list(itertools.chain.from_iterable(documents))
    print(f"Langchain docs:{len(merged_docs)}")
    for i in range(0,len(merged_docs),10):
        batch=merged_docs[i:i+10]
        uploaded=False
        while not uploaded:
            try:
                
                print(f"Uploading from page {i+1} to {i+10}")
                vectorStore.add_documents(documents=batch)
                print(f"Page no. {i} upload completed")
                uploaded=True
                time.sleep(2.5)
            except Exception as e:

                if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                        print("Quota hit! Sleeping for 22 seconds to let the API cool down...")
                        time.sleep(22) 
                        print("Retrying the batch now...")
                else:
                    raise e



        


asyncio.run(webscrapper())
