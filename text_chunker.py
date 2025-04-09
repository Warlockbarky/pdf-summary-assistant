def chunk_text(text, chunk_size):
    """
    Splits text into chunks of specified size, ensuring chunks are split at paragraph boundaries
    and strictly enforcing the chunk size limit.

    Parameters:
        - text (str): The input text to chunk.
        - chunk_size (int): The maximum number of words per chunk.

    Returns:
        - list: A list of text chunks.
    """
    paragraphs = text.split("\n\n")  # Split text into paragraphs
    chunks = []
    current_chunk = []

    for paragraph in paragraphs:
        words = paragraph.split()
        if len(current_chunk) + len(words) <= chunk_size:
            current_chunk.extend(words)
        else:
            # Add the current chunk to the list
            chunks.append(" ".join(current_chunk))
            current_chunk = words

            # If the paragraph itself is too large, split it
            while len(current_chunk) > chunk_size:
                chunks.append(" ".join(current_chunk[:chunk_size]))
                current_chunk = current_chunk[chunk_size:]

    if current_chunk:  # Add the last chunk if it exists
        chunks.append(" ".join(current_chunk))

    return chunks
