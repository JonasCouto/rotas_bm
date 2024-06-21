document.addEventListener("DOMContentLoaded", function () {
    const cepInput = document.getElementById("cep");
    const residenciaInput = document.getElementById("residencia");
    const bairroInput = document.getElementById("bairro");
    const cidadeInput = document.getElementById("cidades");
    const numeroInput = document.getElementById("numero-residencia");
    const latitudeInput = document.getElementById("latitude");
    const longitudeInput = document.getElementById("longitude");

    cepInput.addEventListener("change", function () {
      const cep = this.value.replace(/\D/g, ""); // Remover caracteres não numéricos do CEP

      if (cep.length !== 8) return; // Verificar se o CEP possui o tamanho correto

      fetch(`https://viacep.com.br/ws/${cep}/json/`) // Consultar a API de CEP
        .then((response) => response.json())
        .then((data) => {
          if (!("erro" in data)) {
            // Preencher os campos de endereço, bairro e cidade
            residenciaInput.value = data.logradouro;
            bairroInput.value = data.bairro;
            cidadeInput.value = data.localidade;
            // Atualizar latitude e longitude
            if (
              residenciaInput.value &&
              bairroInput.value &&
              cidadeInput.value &&
              numeroInput.value
            ) {
              const address = `${residenciaInput.value}, ${numeroInput.value}, ${bairroInput.value}, ${cidadeInput.value}`;
              geocodeAddress(address);
            }
          } else {
            alert("CEP não encontrado.");
          }
        })
        .catch((error) => console.error("Erro ao consultar o CEP:", error));
    });

    const formInputs = [
      residenciaInput,
      bairroInput,
      cidadeInput,
      numeroInput,
    ];
    formInputs.forEach((input) => {
      input.addEventListener("change", function () {
        if (
          residenciaInput.value &&
          bairroInput.value &&
          cidadeInput.value &&
          numeroInput.value
        ) {
          const address = `${residenciaInput.value}, ${numeroInput.value}, ${bairroInput.value}, ${cidadeInput.value}`;
          geocodeAddress(address);
        }
      });
    });

    function geocodeAddress(address) {
      const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
        address
      )}`;
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          if (data.length > 0) {
            const location = data[0];
            latitudeInput.value = location.lat;
            longitudeInput.value = location.lon;
          } else {
            console.error("Endereço não encontrado.");
          }
        })
        .catch((error) =>
          console.error("Erro ao consultar o Nominatim:", error)
        );
    }
  });

  function updatePlaceholders() {
    // Atualização do placeholder para Estado Civil
    var estadoCivilSelect = document.getElementById("estado-civil-select");
    var estadoCivilPlaceholderOption =
      estadoCivilSelect.querySelector('option[value="0"]');

    if (window.innerWidth <= 991) {
      estadoCivilPlaceholderOption.textContent = "Estado Civil";
    } else {
      estadoCivilPlaceholderOption.textContent = "Selecione";
    }

    // Atualização do placeholder para Nacionalidade
    var nacionalidadeSelect = document.getElementById(
      "nacionalidade-select"
    );
    var nacionalidadePlaceholderOption =
      nacionalidadeSelect.querySelector('option[value="0"]');

    if (window.innerWidth <= 991) {
      nacionalidadePlaceholderOption.textContent = "Nacionalidade";
    } else {
      nacionalidadePlaceholderOption.textContent = "Selecione";
    }

    // Atualização do placeholder para Gênero
    var generoSelect = document.getElementById('genero-select');
    var generoPlaceholderOption = generoSelect.querySelector('option[class="placeholder-mobile"]');
    if (window.innerWidth <= 991) {
        generoPlaceholderOption.textContent = 'Genero';
    } else {
        generoPlaceholderOption.textContent = 'Selecione';
    }
      // Atualização do placeholder para Data de Nascimento
      var dataNascimentoInput = $('#data-nascimento');
    
      if (window.innerWidth <= 991) {
          dataNascimentoInput.attr('type', 'date');
        
      } else {
          dataNascimentoInput.attr('type', 'text');
         
      }
    
  }


  $('#data-nascimento').on('focus', function() {
    if ($(window).width() <= 991) {
      this.type = 'date';
        
    }
  }).on('blur', function() {
    if ($(window).width() <= 991) {
      this.type = 'text';
    }else{
      this.type = 'date'
    }

});
// Executar a função ao carregar a página e quando a janela for redimensionada
document.addEventListener('DOMContentLoaded', updatePlaceholders);
window.addEventListener('resize', updatePlaceholders);

$(document).ready(function(){
    $('#cidade').on('input', function() {
        var termo = $(this).val();
        if (termo.length > 2) {
            $.ajax({
                url: '/login/buscar_cidades/',
                data: {
                    'termo': termo
                },
                success: function(data) {
                    $('#dropdown').empty().show();
                    data.forEach(function(cidade) {
                        $('#dropdown').append('<div class="dropdown-item" data-value="' + cidade.nome + ' (' + cidade.estado + ')' + '">' + cidade.nome + ' (' + cidade.estado + ')</div>');
                    });
                }
            });
        } else {
            $('#dropdown').empty().hide();
        }
    });

    $(document).on('click', '.dropdown-item', function() {
        var value = $(this).data('value');
        $('#cidade').val(value);
        $('#dropdown').hide();
        $('.error-message').hide();
    });

    $('#cidade').on('change', function() {
        var value = $(this).val();
        var exists = $('.dropdown-item').filter(function() {
            return $(this).data('value').toLowerCase() === value.toLowerCase();
        }).length;
        if (!exists) {
            $(this).val('');
        } 
    });

    $(document).click(function(e) {
      if (!$(e.target).closest('.select-style').length) {
          $('#dropdown').hide();
      }
  });
});
