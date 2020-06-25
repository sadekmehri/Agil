function success(msg){
      if(!msg){ msg = "Please enter a message";}
      new Noty({
        theme: ' alert bg-success text-white alert-styled-left p-0',
        text: msg,
        type: 'success',
        progressBar: true,
        layout: 'topRight',
        timeout: 2500,
        closeWith: ['button']
    }).show();
}

function error(msg){
    if(!msg){ msg = "Please enter a message";}
       new Noty({
       theme: ' alert bg-danger text-white alert-styled-left p-0',
       text: msg,
       type: 'error',
       progressBar: true,
       layout: 'topRight',
       timeout: 2500,
       closeWith: ['button']
   }).show();
}


function warning(msg){
    if(!msg){ msg = "Please enter a message";}
       new Noty({
       theme: ' alert bg-warning text-white alert-styled-left p-0',
       text: msg,
       type: 'warning',
       progressBar: true,
       layout: 'topRight',
       timeout: 2500,
       closeWith: ['button']
   }).show();
}


function currrent_date() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();
    return (yyyy + '-' + mm + '-' + dd);
}