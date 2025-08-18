from typing import List, Dict, Union

# 重新定义 Document 类型以保持一致
Document = Dict[str, Union[str, Dict]]

def split_text_by_character(document: Document, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    将单个文档的文本内容按字符分割成多个块 (chunks)。

    Args:
        document (Document): 包含 "page_content" 和 "metadata" 的文档字典。
        chunk_size (int): 每个块的最大字符数。
        chunk_overlap (int): 相邻块之间的重叠字符数。

    Returns:
        List[Document]: 一个由分割后的文本块组成的文档列表。
                         每个块都继承了原始文档的元数据。
    """
    if not isinstance(document, dict) or "page_content" not in document:
        raise ValueError("Input must be a Document dictionary with a 'page_content' key.")

    text = document["page_content"]
    metadata = document["metadata"]
    
    if len(text) <= chunk_size:
        return [document]

    chunks = []
    start_index = 0
    
    while start_index < len(text):
        end_index = start_index + chunk_size
        chunk_text = text[start_index:end_index]
        
        # 为了区分每个 chunk，我们可以在 metadata 中添加一些信息
        chunk_metadata = metadata.copy()
        chunk_metadata["chunk_number"] = len(chunks) + 1
        
        chunks.append({
            "page_content": chunk_text,
            "metadata": chunk_metadata
        })
        
        # 如果已经到达文本末尾，则退出循环
        if end_index >= len(text):
            break
            
        # 下一个块的起始位置要考虑重叠
        start_index += chunk_size - chunk_overlap

    return chunks

# --- 使用示例 ---
if __name__ == '__main__':
    # 1. 创建一个示例文本
    long_text = "This is a very long text designed to test the character splitter. " * 100
    long_text += "The goal is to see how it breaks down the content into smaller, manageable chunks. " * 50
    long_text += "Each chunk should have a specific size and overlap with the next one. " * 50
    long_text += "This ensures that context is not lost at the boundaries of the chunks. The end."

    sample_doc = {
        "page_content": long_text,
        "metadata": {"source": "test_document.txt"}
    }

    print(f"Original document length: {len(sample_doc['page_content'])} characters")
    print("-" * 20)

    # 2. 使用默认参数进行分割
    print("--- Splitting with default settings (chunk_size=1000, chunk_overlap=200) ---")
    chunks = split_text_by_character(sample_doc)
    
    print(f"Number of chunks created: {len(chunks)}")
    
    # 打印第一个块的信息
    print("\n--- First Chunk ---")
    print(f"Content: '{chunks[0]['page_content'][:100]}...'")
    print(f"Length: {len(chunks[0]['page_content'])}")
    print(f"Metadata: {chunks[0]['metadata']}")

    # 打印第二个块的信息，并检查重叠部分
    if len(chunks) > 1:
        print("\n--- Second Chunk ---")
        print(f"Content: '{chunks[1]['page_content'][:100]}...'")
        print(f"Length: {len(chunks[1]['page_content'])}")
        print(f"Metadata: {chunks[1]['metadata']}")

        # 验证重叠
        overlap_start_of_chunk2 = chunks[1]['page_content'][:200]
        overlap_end_of_chunk1 = chunks[0]['page_content'][-200:]
        print(f"\nOverlap check: {'Overlap is correct.' if overlap_start_of_chunk2 == overlap_end_of_chunk1 else 'Overlap is incorrect.'}")

    # 3. 使用自定义参数进行分割
    print("\n--- Splitting with custom settings (chunk_size=500, chunk_overlap=50) ---")
    custom_chunks = split_text_by_character(sample_doc, chunk_size=500, chunk_overlap=50)
    print(f"Number of chunks created: {len(custom_chunks)}")
    print(f"Length of first chunk: {len(custom_chunks[0]['page_content'])}")
