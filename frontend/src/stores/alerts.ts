import Swal from 'sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'
import { defineStore } from 'pinia'

const alertTemplate = Swal.mixin({
    toast: true,
    position: 'bottom-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true
})

export const useAlertStore = defineStore('alerts', {
    actions: {
        showSuccessAlert(title: string) {
            alertTemplate.fire({
                icon: 'success',
                title: title
            })
        },
        showErrorAlert(error: string) {
            alertTemplate.fire({
                icon: 'error', 
                title: error
            })
        }
    }
})