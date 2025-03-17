import streamlit as st
import json
import time

# File to store library data
LIBRARY_FILE = "library.json"

def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, generation, read):
    library.append({"title": title, "author": author, "year": year, "generation": generation, "read": read
    })
    save_library(library)
    st.success(f"✅ '{title}' added successfully!")
    time.sleep(1)
    st.rerun()

def remove_book(library, title):
    updated_library = [book for book in library if book["title"].lower() != title.lower()]
    if len(updated_library) < len(library):
        save_library(updated_library)
        return True
    return False

def search_books(library, search_term, by="title"):
    return [book for book in library if search_term.lower() in book[by].lower()]

def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"] == "yes")
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, read_percentage

def main():
    st.set_page_config(page_title="Personal Library Manager", page_icon="📚")
    st.title("📚 PERSONAL LIBRARY MANAGER")
    st.markdown("The management of your book collection with this user-friendly and efficient tool.")
    
    library = load_library()
    
    menu = [
            "📖 Add Book",
            "🗑️ Remove Book",
            "🔍 Search Book",
            "📚 Display All Books",
            "📊 Statistics", 
            "❌ Exit"
            ]
    
    # Added the selectbox for the sidebar
    st.sidebar.markdown("Welcome to your Personal Library Manager")
    choice = st.sidebar.selectbox("Enter your choice:", menu)
    
    
    if choice == "📖 Add Book":
        st.subheader("➕ Add a New Book")
        with st.form("add_book_form", clear_on_submit=True):
            title = st.text_input("Title", placeholder="Enter book title")
            author = st.text_input("Author", placeholder="Enter author's name")
            year = st.number_input("Publication Year", min_value=0, step=1)
            generation = st.text_input("Genre", placeholder="Enter book generation")
            read = st.radio("Have you read this book?", ("yes", "no"), index=1) 
            submitted = st.form_submit_button("Add Book")
            if submitted and title and author and generation:
                add_book(library, title, author, year, generation, read)
            elif submitted:
                st.warning("⚠️ Please fill in all fields.")
    
    elif choice == "🗑️ Remove Book":
        st.subheader("🗑 Remove a Book")
        title = st.text_input("Enter the title of the book to remove", placeholder="Book title")
        if st.button("Remove Book", use_container_width=True):
            if remove_book(library, title):
                st.success(f"✅ '{title}' removed successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("⚠️ Book not found.")
    
    elif choice == "🔍 Search Book":
        st.subheader("🔎 Search for a Book")
    
        search_by = st.radio("Search by:", ["Title", "Author"], index=0)  # Default to Title
        search_by_choice = 1 if search_by == "Author" else 0  # Set the index for search term

        st.write("Enter your choice:", search_by_choice + 1)  # Display the search type number
        
        if search_by_choice == 0:  # Search by title
            search_term = st.text_input("Enter the title:")
        else:  # Search by author
            search_term = st.text_input("Enter the author:")
        
        if st.button("Search", use_container_width=True):
            results = search_books(library, search_term, by="title" if search_by_choice == 0 else "author")
            if results:
                st.write("Matching Books:")
                for i, book in enumerate(results, 1):
                    st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['generation']} - {'✅ Read' if book['read'] == 'yes' else '❌ Unread'}")
            else:
                st.warning("⚠️ No matching books found.")

    elif choice == "📚 Display All Books":
        st.subheader("📖 Your Library Collection")
        if library:
            st.write("Your Library:")
            for idx, book in enumerate(library, 1):  # Enumerate for 1-based index
                st.write(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['generation']} - {'✅ Read' if book['read'] == 'yes' else '❌ Unread'}")
        else:
            st.info("ℹ️ Your library is empty.")

    elif choice == "📊 Statistics":
        st.subheader("📈 Library Statistics")
        total_books, read_percentage = display_statistics(library)
        col1, col2 = st.columns(2)
        col1.metric("📚 Total Books", total_books)
        col2.metric("📖 Percentage Read", f"{read_percentage:.2f}%")
    
    elif choice == "❌ Exit":
        st.info("👋 Library saved to file. Goodbye!")
        st.stop()  # Stops the app

if __name__ == "__main__":
    main()
