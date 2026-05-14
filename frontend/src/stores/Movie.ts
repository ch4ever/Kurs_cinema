import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import api from '../api/api'

type Franchise = {
    id: number
    name: string
    description: string
}
type Actor = {
    id: number
    name: string
}
type Genre = {
    id: number
    name: string
}
type Review = {
    id: number
    rating: number
    text: string
    created_at: number
}

type Movie = {
    id: number
    title: string
    description: string
    release_date: string
    franchise: Franchise | null
    rating: number
    genre: Genre[]
    director: string
    actors: Actor[]
    reviews: Review[]
}

export const useMovieStore = defineStore('movie', {
    state: () => ({
        movies: [] as Movie[],
        movie: null as Movie | null,
        loading: false,
    }),
    actions: {
        async getMovies() {
            this.loading = true
            try{
                const { data } = await api.get<Movie[]>('movies/')
                this.movies = data
            }
            catch (error) {
                console.error(error)
            }
            finally {
                this.loading = false
            }
        },
        async getMovie(id: number) {
            this.loading = true
            try{
                const { data } = await api.get<Movie>(`movies/${id}/`)
                this.movie = data
            }
            catch (error) {
                console.error(error)
            }
            finally {
                this.loading = false
            }
        },
        async createMovie(movie: Movie) {
            try{
                const { data } = await api.post<Movie>('movies/', movie)
                this.movie = data
            }
            catch (error) {
                console.error(error)
            }
            finally {
                this.loading = false
            }
        },
        async updateMovie(id: number, movie: Movie) {
            try{
                const { data } = await api.put<Movie>(`movies/${id}/`, movie)
                this.movie = data
            }
            catch (error) {
                console.error(error)
            }
            finally {
                this.loading = false
            }
        },
        async deleteMovie(id: number) {
            try{
                await api.delete(`movies/${id}/`)
                this.movies = this.movies.filter(movie => movie.id !== id)
            }
            catch (error) {
                console.error(error)
            }
            finally {
                this.loading = false
            }
        }
    }
})