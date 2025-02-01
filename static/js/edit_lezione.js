document.addEventListener('DOMContentLoaded', function() {
    // Inizializzare i select di Materialize
    var elems = document.querySelectorAll('select');
    M.FormSelect.init(elems);
    
    // Inizializzare le textarea
    var textareas = document.querySelectorAll('.materialize-textarea');
    textareas.forEach(function(textarea) {
        M.textareaAutoResize(textarea);
    });
    
    // Template per un nuovo tutor
    function createTutorEntry() {
        var template = document.querySelector('.tutor-entry');
        if (!template) {
            console.error('Template tutor-entry non trovato');
            return null;
        }
        
        var clone = template.cloneNode(true);
        
        // Reset dei valori
        clone.querySelectorAll('input, textarea').forEach(function(el) {
            el.value = '';
            if (el.classList.contains('materialize-textarea')) {
                M.textareaAutoResize(el);
            }
        });
        
        // Reset e reinizializzazione del select
        var select = clone.querySelector('select');
        if (select) {
            select.selectedIndex = 0;
            M.FormSelect.init(select);
        }
        
        return clone;
    }
    
    // Gestione aggiunta tutor
    document.getElementById('add-tutor').addEventListener('click', function() {
        var tutorList = document.getElementById('tutor-list');
        var newEntry = createTutorEntry();
        
        if (newEntry && tutorList) {
            tutorList.appendChild(newEntry);
            
            // Reinizializzare i componenti Materialize nel nuovo elemento
            M.FormSelect.init(newEntry.querySelectorAll('select'));
            M.updateTextFields();
        }
    });
    
    // Gestione rimozione tutor
    document.addEventListener('click', function(e) {
        if (e.target.closest('.remove-tutor')) {
            var entry = e.target.closest('.tutor-entry');
            var tutorList = document.getElementById('tutor-list');
            
            if (entry && tutorList && tutorList.children.length > 1) {
                entry.remove();
            } else if (tutorList.children.length <= 1) {
                // Mostra un messaggio se si tenta di rimuovere l'ultimo tutor
                M.toast({
                    html: 'È necessario mantenere almeno un tutor',
                    classes: 'red'
                });
            }
        }
    });
    
    // Validazione del form
    document.querySelector('form').addEventListener('submit', function(e) {
        var tutorSelects = document.querySelectorAll('select[name="tutor_ids[]"]');
        var selectedTutors = new Set();
        var hasError = false;
        
        tutorSelects.forEach(function(select) {
            var tutorId = select.value;
            if (tutorId) {
                if (selectedTutors.has(tutorId)) {
                    hasError = true;
                    M.toast({
                        html: 'Non è possibile selezionare lo stesso tutor più volte',
                        classes: 'red'
                    });
                }
                selectedTutors.add(tutorId);
            }
        });
        
        if (hasError) {
            e.preventDefault();
        }
    });
});