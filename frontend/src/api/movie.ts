import type { Movie, MovieCreatePayload, MovieUpdatePayload } from "@/types/movie"
import api from './api'

export const MovieService = {
    getAll() {
        return api.get<Movie[]>('movies/')
    },
    getById(id: number) {
        return api.get<Movie>(`movies/${id}/`)
    },
    create(movieData: MovieCreatePayload) {
        return api.post<Movie>('movies/', movieData)
    },
    update(id: number, movieData: MovieUpdatePayload) {
        return api.put<Movie>(`movies/${id}/`, movieData)
    },
    delete(id: number) {
        return api.delete(`movies/${id}/`)
    }
}
