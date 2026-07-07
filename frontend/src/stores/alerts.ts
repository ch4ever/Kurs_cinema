import Swal from 'sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'
import { defineStore } from 'pinia'

// function escapeHtml(value: string) {
//     const escapeMap: Record<string, string> = {
//         '&': '&amp;',
//         '<': '&lt;',
//         '>': '&gt;',
//         '"': '&quot;',
//         "'": '&#039;',
//     }

//     return value.replace(/[&<>"']/g, (char) => escapeMap[char] ?? char)
// }

// function formatMessage(message: string) {
//     return escapeHtml(message).replace(/\n/g, '<br>')
// }

const alertTemplate = Swal.mixin({
    toast: true,
    position: 'bottom-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    customClass: {
        popup: 'app-alert',
        title: 'app-alert-title',
        timerProgressBar: 'app-alert-progress',
      },
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
                // html: formatMessage(error)
            })
        }
    }
})
