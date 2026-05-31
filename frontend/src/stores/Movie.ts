import { defineStore } from 'pinia'
import type { Movie, MovieCreatePayload, MovieUpdatePayload } from "@/types/movie"
import {MovieService} from "@/api/movie"
import { useAlertStore } from '@/stores/alerts'




export const useMovieStore = defineStore('movie', {
    state: () => ({
        movies: [] as Movie[],
        movie: null as Movie | null,
        loading: false,
        
    }),

    actions: {
        async fetchMovies() {
            this.loading = true
            const alerts = useAlertStore()

            try{
                const { data } = await MovieService.getAll()
                this.movies = data
            }
            catch (error: any) {
                const errorMsg = error.response?.data?.error || 'Error while getting films'
                alerts.showErrorAlert(errorMsg)
                throw error
                
            }
            finally {
                this.loading = false
            }
        },
        async getMovie(id: number) {
            this.loading = true
            const alerts = useAlertStore()

            try{
                const { data } = await MovieService.getById(id)
                this.movie = data
            }
            catch (error: any) {
                const errorMsg = error.response?.data?.error || 'Error while getting film'
                alerts.showErrorAlert(errorMsg)
                throw error
            }
            finally {
                this.loading = false
            }
        },

        async createMovie(movie: MovieCreatePayload) {
            this.loading = true
            const alerts = useAlertStore()
            try{
                const { data } = await MovieService.create(movie)
                this.movies.push(data)
                return data
            }
            catch (error: any) {
                const errorMsg = error.response?.data?.error || 'Error while getting film'
                alerts.showErrorAlert(errorMsg)
                throw error
            }
            finally {
                this.loading = false
            }
            
        },

        async updateMovie(id: number, movie: MovieUpdatePayload) {
            this.loading = true
            const alerts = useAlertStore()
            try{
                const { data } = await MovieService.update(id, movie)
                this.movie = data
                return data
            }
            catch (error: any) {
                const errorMsg = error.response?.data?.error || 'Error while updating film'
                alerts.showErrorAlert(errorMsg)
                throw error
            }
            finally {
                this.loading = false
            }
        },

        async deleteMovie(id: number) {
            this.loading = true
            const alerts = useAlertStore()

            try{
                await MovieService.delete(id)
                this.movies = this.movies.filter(movie => movie.id !== id)
            }
            catch (error: any) {
                const errorMsg = error.response?.data?.error || 'Error while deleting film'
                alerts.showErrorAlert(errorMsg)
                throw error
            }
            finally {
                this.loading = false
            }
        }
    }
})
