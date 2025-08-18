from pathlib import Path
from typing import List, Dict, Union

# 为了简单起见，我们先定义一个 Document 类型
# 在 LangChain 中，这通常是一个具有 page_content 和 metadata 的对象
Document = Dict[str, Union[str, Dict]]

def load_text_document(file_path: Union[str, Path]) -> Document:
    """
    加载单个文本文件并返回其内容。

    Args:
        file_path (Union[str, Path]): 文本文件的路径。

    Returns:
        Document: 一个包含文件内容和元数据的字典。
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found at: {path}")

    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # metadata 包含了关于文档来源的信息，这在 RAG 中非常重要
        metadata = {"source": str(path)}
        
        return {"page_content": text, "metadata": metadata}
    except Exception as e:
        print(f"Error loading file {path}: {e}")
        return None

def load_directory(directory_path: Union[str, Path], glob_pattern: str = "*.txt") -> List[Document]:
    """
    加载目录下所有匹配 glob 模式的文本文件。

    Args:
        directory_path (Union[str, Path]): 目标目录的路径。
        glob_pattern (str): 用于匹配文件的 glob 模式，默认为 "*.txt"。

    Returns:
        List[Document]: 一个包含所有已加载文档的列表。
    """
    path = Path(directory_path)
    if not path.is_dir():
        raise NotADirectoryError(f"Directory not found at: {path}")

    documents = []
    for file_path in path.glob(glob_pattern):
        if file_path.is_file():
            doc = load_text_document(file_path)
            if doc:
                documents.append(doc)
    
    return documents

# --- 使用示例 ---
if __name__ == '__main__':
    # 创建一个临时目录和一些示例文本文件用于测试
    temp_dir = Path("./temp_docs")
    temp_dir.mkdir(exist_ok=True)
    
    (temp_dir / "doc1.txt").write_text("This is the first document about AI.")
    (temp_dir / "doc2.txt").write_text("The second document discusses machine learning.")
    (temp_dir / "notes.md").write_text("# Notes\nThis is a markdown file.")

    print(f"Created temporary directory: {temp_dir.resolve()}")

    # 1. 测试加载单个文件
    print("\n--- Loading a single document ---")
    try:
        single_doc = load_text_document(temp_dir / "doc1.txt")
        print(single_doc)
    except FileNotFoundError as e:
        print(e)

    # 2. 测试加载整个目录
    print("\n--- Loading all .txt documents from a directory ---")
    try:
        all_docs = load_directory(temp_dir)
        for doc in all_docs:
            print(doc)
    except NotADirectoryError as e:
        print(e)
        
    # 3. 测试加载不同类型的文件
    print("\n--- Loading all .md documents from a directory ---")
    try:
        md_docs = load_directory(temp_dir, glob_pattern="*.md")
        print(md_docs[0])
    except Exception as e:
        print(e)

    # 清理临时文件
    import shutil
    shutil.rmtree(temp_dir)
    print(f"\nCleaned up temporary directory: {temp_dir.resolve()}")
