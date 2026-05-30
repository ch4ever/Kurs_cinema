import { defineStore } from 'pinia'
import type { Movie, MovieCreatePayload, MovieUpdatePayload } from "@/types/movie"
import {MovieService} from "@/api/movie"



export const useMovieStore = defineStore('movie', {
    state: () => ({
        movies: [] as Movie[],
        movie: null as Movie | null,
        loading: false,
        error: null as string | null,
    }),

    actions: {
        async fetchMovies() {
            this.loading = true
            this.error = ''
            try{
                const { data } = await MovieService.getAll()
                this.movies = data
            }
            catch (error) {
                this.error = String(error)
                throw error
                
            }
            finally {
                this.loading = false
            }
        },
        async getMovie(id: number) {
            this.loading = true
            try{
                const { data } = await MovieService.getById(id)
                this.movie = data
            }
            catch (error) {
                this.error = String(error)
                throw error
            }
            finally {
                this.loading = false
            }
        },

        async createMovie(movie: MovieCreatePayload) {
            try{
                const { data } = await MovieService.create(movie)
                this.movies.push(data)
            }
            catch (error) {
                this.error = String(error)
                throw error
            }
            finally {
                this.loading = false
            }
            
        },

        async updateMovie(id: number, movie: MovieUpdatePayload) {
            try{
                const { data } = await MovieService.update(id, movie)
                this.movie = data
            }
            catch (error) {
                this.error = String(error)
                throw error
            }
            finally {
                this.loading = false
            }
        },

        async deleteMovie(id: number) {
            try{
                await MovieService.delete(id)
                this.movies = this.movies.filter(movie => movie.id !== id)
            }
            catch (error) {
                this.error = String(error)
                throw error
            }
            finally {
                this.loading = false
            }
        }
    }
})
