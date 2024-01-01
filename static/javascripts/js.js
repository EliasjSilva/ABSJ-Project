  // Atualiza a data a cada segundo
  function atualizarData() {
    var now = new Date();
    var formattedDate = now.toLocaleString(); // ou qualquer formato desejado

    // Atualiza o conteúdo HTML com a nova data
    $('#data-atual').text(formattedDate);
  }

  // Chama a função inicialmente e a cada segundo
  $(document).ready(function() {
    atualizarData();
    setInterval(atualizarData, 1000); // Atualiza a cada segundo
  });

// POP UP INFO
function togglePopup(tipo) {
  if (tipo == 'vencido') {
    $('.message_vencido').toggle(50);
    $('.message_prazo').hide();
  } 
  else if (tipo == 'prazo') {
    $('.message_prazo').toggle(50);
    $('.message_vencido').hide();
  } 
  else if (tipo == 'categoria') {
    $('.delete').toggle(50);
  } 
  else if (tipo == 'contribuidor') {
    $('.delete').toggle(50);
  } 
  else if (tipo == 'produto') {
    $('.delete').toggle(50);
  } 
  else {
    // Se o tipo não for 'vencido' ou 'prazo', você pode ocultar ambos
    $('.message_vencido, .message_prazo').hide();
  }
}
