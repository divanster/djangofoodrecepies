CKEDITOR.editorConfig = function( config ) {
    // Define the toolbar options
    config.toolbarGroups = [
        { name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
        { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
        { name: 'editing', groups: [ 'find', 'selection', 'spellchecker' ] },
        { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
        { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
        { name: 'links', groups: [ 'links' ] },
        { name: 'insert', groups: [ 'insert' ] },
        { name: 'styles', groups: [ 'styles' ] },
        { name: 'colors', groups: [ 'colors' ] },
        { name: 'tools', groups: [ 'tools' ] },
        { name: 'others', groups: [ 'others' ] },
        { name: 'about', groups: [ 'about' ] }
    ];

    // Define which buttons are included in the toolbar
    config.removeButtons = 'NewPage,ExportPdf,Print,Form,Checkbox,Radio,TextField,Textarea,Select,Button,ImageButton,HiddenField,Scayt,CreateDiv,Language,Flash,Smiley,Iframe,About';

    // Enable the editor to resize automatically
    config.resize_enabled = true;

    // Enable word count plugin
    config.wordcount = {
        showParagraphs: false,
        showWordCount: true,
        showCharCount: true,
        countSpacesAsChars: true
    };
};
