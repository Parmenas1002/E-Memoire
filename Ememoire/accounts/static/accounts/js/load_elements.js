// Load Faculty options
$("#id_university").change(function () {
    const url = $("#studentForm").attr("data-faculty-url");  // Récupérer l'Url load_faculty
    const universityId = $(this).val();  // Récupérer l'ID de l'entité 

    if (universityId == "")
    {
        let html_data_false = '<option value="">-----------</option>';
        $("#id_faculty").html(html_data_false);
        $("#id_entity").html(html_data_false);
        $("#id_option").html(html_data_false);
    }

    else
    {
        $.ajax({                       // Initialiser la requete AJAX
            url: url,                    // Ajouter l'URL de la requete
            data: {
                'university_id': universityId       // Ajouter l'ID de l'université aux paramètres GET
            },
            success: function (data) { 
                let html_data = '<option value="">-----------</option>';
                data.forEach(function (faculty) {
                    html_data += `<option value="${faculty.id}">${faculty.name}</option>`
                });
                console.log(html_data);
                $("#id_faculty").html(html_data)         
            }
        });
    }
});

//Load Faculty
$("#id_faculty").change(function () {
    const url = $("#studentForm").attr("data-entity-url");  
    const facultyId = $(this).val(); 

    if (facultyId == "")
    {
        let html_data_false = '<option value="">-----------</option>';
        $("#id_entity").html(html_data_false);
        $("#id_option").html(html_data_false);
    }
    else
    {
        $.ajax({                       
            url: url,                    
            data: {
                'faculty_id': facultyId      
            },
            success: function (data) {   
                let html_data = '<option value="">-----------</option>';
                data.forEach(function (entity) {
                    html_data += `<option value="${entity.id}">${entity.name}</option>`
                });
                console.log(html_data);
                $("#id_entity").html(html_data);               
            }
        });
    }
});

// Load Options of Entity
$("#id_entity").change(function () {
    const url = $("#studentForm").attr("data-options-url");  
    const entityId = $(this).val();

    if (entityId == "")
    {
        let html_data_false = '<option value="">-----------</option>';
        $("#id_option").html(html_data_false);
    }
    else
    {
        $.ajax({                       
            url: url,                    
            data: {
                'entity_id': entityId       
            },
            success: function (data) {
                let html_data = '<option value="">-----------</option>';
                data.forEach(function (option) {
                    html_data += `<option value="${option.id}">${option.name}</option>`
                });
                console.log(html_data);
                $("#id_option").html(html_data);
    
                
            }
        });
    }    
});

