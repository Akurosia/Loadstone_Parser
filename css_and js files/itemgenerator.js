cvs_row = [];
window.onload = function() {
        var $rows = $('#table tr');
        $rows.splice(0,1);
        //when button is pressed
        $('#searchbtn').click(function() {
                var val = $.trim($('#search').val()).replace(/ +/g, ' ').toLowerCase();
                // hides each element which returns "true"
                $rows.show().filter(function() {
                        //from each row(tr) get all child elements(td), select last one(e.g. td:6), get child element (input) and get value (checked)
                        var checkbox = $(this).children().last().children().is(':checked')
                        var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
                        return (!~text.indexOf(val) && !checkbox);
                }).hide();
        });

        //when enter is pressed while input field is focused
        $('#search').keypress(function(e){
                if(e.which == 13){
                        $('#searchbtn').click();
                }
        });

        $('#selectbtn').click(function() {
                mySelect(true);
        });

        $('#unselectbtn').click(function() {
                mySelect(false);
        });

        function mySelect(state) {
                var $myrows  = $('#table tr');
                $myrows.splice(0,1);
                $myrows.filter(function() {
                        var rowIsDisplayed = $(this).is(':visible');
                        if(rowIsDisplayed == true){
                                $(this).children().last().children().prop('checked', state);
                        }
                })
        }
        //
        // EXPORT AS CSV CODE
        //
        function getTableContent(){
                csv = [];
                var $myrows  = $('#table tr');
                $myrows.filter(function() {
                        var rowIsDisplayed = $(this).is(':visible');
                        if(rowIsDisplayed == true){
                                $mycells = $(this).find("td,th")
                                cvs_row.length = 0;
                                $mycells.filter(function() {
                                        var imgele = $(this).find("span").find("img")
                                        var cbele = $(this).find("input")
                                        text = "\"" + $(this).text().trim()
                                        if(imgele.length > 0){
                                                text = text + " HQ";
                                        }
                                        if(cbele.length > 0){
                                                text = "\""+cbele.is(':checked')
                                        }
                                        cvs_row.push(text + "\"");
                                })
                                csv.push(cvs_row.join(";"));
                        }
                })
                output = csv.join("\n");
                console.log(output);
                return output;
        };

        $('#export2CSV').click(function() {
                getFile(getTableContent());
        });

        function getFile(data){
                var downloadLink = document.createElement("a");
                var blob = new Blob(["\ufeff", data]);
                var url = URL.createObjectURL(blob);
                downloadLink.href = url;
                downloadLink.download = "FFXIV_Item_Data.csv";
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
        };
}




