$(function(){
    $("body").html(`
<center>
    <input type="submit" value="Adelante" id="forward"/>
    <table>
        <tr>
            <td>
                <input type="submit" value="Izquierda" id="left"/>
            </td>
            <td>
                <input type="submit" value="Parar" id="stop"/>
            </td>
            <td>
                <input type="submit" value="Derecha" id="right"/>
                </form>
            </td>
        </tr>
    </table>
    <input type="submit" value="Atras" id="backward"/>
</center>

<input type="submit" value="Mostrar Cara" id="mode" />

`);
    const showFace = "Mostrar Cara";
    const showInfo = "Mostrar Info";
    ["left", "right", "forward", "backward", "stop"].forEach(function (each){
        var element = $("#"+each);
        element.click(function(e){
            callToServer("./"+each);
            element.fadeTo(200, 0.3);
            element.fadeTo(200, 1);
        });
    });
    $("#mode").on( "click", function() {
        let input = $("#mode");
        let shouldShowFace = input.val() == showFace;
        if(shouldShowFace){
            callToServer('./showFace');
            input.val(showInfo);
        }else{
            callToServer('./showInfo');
            input.val(showFace);
        }
        
    });
})
function callToServer(path){
    console.log(path);
    $.ajax({url: path, success: function(result){
        console.log("exito")
    }});
}