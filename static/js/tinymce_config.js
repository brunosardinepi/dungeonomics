<script type="text/javascript">
    var monsters = [];
    var monsters_dict = {{monsters|safe}};
    for (var key in monsters_dict) {
        monsters.push({
                'id': monsters_dict[key],
                'name': key,
                'type': 'monster'
            });
    }
    tinymce.init({
        selector: "#id_content",
        height : "350",
        plugins: [
        'paste autosave autolink print searchreplace table textcolor wordcount link image mention'
        ],
        menu: {
        edit: {title: 'Edit', items: 'undo redo | cut copy paste pastetext | selectall | searchreplace'},
        insert: {title: 'Insert', items: 'image'},
        view: {title: 'View', items: 'visualaid'},
        format: {title: 'Format', items: 'bold italic underline strikethrough superscript subscript | formats | removeformat'},
        table: {title: 'Table', items: 'inserttable tableprops deletetable | cell row column'}
        },
        toolbar: 'print | fontsizeselect bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link | forecolor backcolor',
        browser_spellcheck: true,
        paste_as_text: true,
        fontsize_formats: "8pt 10pt 12pt 14pt 18pt 24pt 36pt",
        mentions: {
            source: monsters,
            delay: 0,
            insert: function(item) {
                var url = "{% url 'characters:monster_detail' monster_pk=999999999999 %}".replace(999999999999, item.id);
                return "<a href=" + url + ">" + item.name + "</a>";
            }
        }
    });
</script>