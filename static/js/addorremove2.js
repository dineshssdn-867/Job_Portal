function addorremove(id) {
        if (id){
            $.ajax({
                success:function () {
                    const Toast = Swal.mixin({
                      toast: true,
                      position: 'top',
                      showConfirmButton: true,
                      timer: 2000,
                      timerProgressBar: true,
                      onOpen: (toast) => {
                        toast.addEventListener('mouseenter', Swal.stopTimer)
                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                      }
                    })

                    Toast.fire({
                      icon: 'error',
                      title: 'You are not an employee!'
                    })

                }

            });
        }
    }