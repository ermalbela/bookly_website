import type { BookDetail, Book, BookCreateModel } from '@/types/book_types'
import api from './api'


export const bookService = {
  get_all_books: async (): Promise<BookDetail[]> => {
    const { data } = await api.get<BookDetail[]>('/books/')
    return data
  },

  get_books_by_user: async (user_uid: string) => {
    const { data } = await api.get<Book[]>(`/books/${user_uid}`);
    console.log(data);
    return data
  },

  get_book_by_id: async (book_uid: string): Promise<BookDetail> => {
    const { data } = await api.get<BookDetail>(`/books/${book_uid}`)
    return data
  },

  create_book: async (book_data: BookCreateModel): Promise<Book> => {
    const { data } = await api.post('/books/', book_data)
    return data
  },

  update_book: async (id: string, book_update_data: Partial<BookCreateModel>): Promise<Book> => {
    const { data } = await api.patch<Book>(`/books/${id}`, book_update_data)
    return data
  },

  delete_book: async (book_uid: string): Promise<void> => {
    await api.delete(`/books/${book_uid}`)
  },
}