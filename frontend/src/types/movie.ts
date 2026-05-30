export type Franchise = {
    id: number
    name: string
    description: string
}
export type Actor = {
    id: number
    name: string
}
export type Genre = {
    id: number
    name: string
}
export type Review = {
    id: number
    rating: number
    text: string
    created_at: number
}

export type Movie = {
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
    poster: string | null
}

export type MovieCreatePayload = FormData
export type MovieUpdatePayload = FormData
