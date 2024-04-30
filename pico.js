$(function(){
    
    $("<body>").html(`
<center><b>
    <form action="./forward">
        <input type="submit" value="Adelante" />
    </form>
    <table>
        <tr>
            <td>
                <form action="./left">
                    <input type="submit" value="Izquierda" />
                </form>
            </td>
            <td>
                <form action="./stop">
                    <input type="submit" value="Parar" />
                </form>
            </td>
            <td>
                <form action="./right">
                    <input type="submit" value="Derecha" />
                </form>
            </td>
        </tr>
    </table>
    <form action="./back">
        <input type="submit" value="Back" />
    </form>
</center>

<form action="./grabar">
<input type="submit" value="Grabar" class="grabar" />
</form>

<form action="./pararGrabacion">
<input type="submit" value="Parar Grabacion" class="pararGrabacion" />
</form>
`)
})