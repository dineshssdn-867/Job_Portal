function addorremove(id) {
        if (id){
        var wishlist= $('#jobwl'+id).data('wl');
        if(wishlist == 0 ){
            $.ajax({
                url:"/users/add-wishlist/" +id,
                method:"GET",
                success:function () {
                    $('#jobwl'+id).removeClass('btn-primary').addClass('btn-danger')
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
                      icon: 'success',
                      title: 'You added!'
                    })
                    $('#jobwl'+id).data('wl',1);


                }

            });
            }else{

            $.ajax({
                url:"/users/remove-from-wishlist/" +id,
                method:"GET",
                success:function () {
                    $('#jobwl'+id).removeClass('btn-danger').addClass('btn-primary')
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
                      icon: 'success',
                      title: 'You Removed!'
                    })
                     $('#jobwl'+id).data('wl',0);

                }

            });

            }
        }
    }