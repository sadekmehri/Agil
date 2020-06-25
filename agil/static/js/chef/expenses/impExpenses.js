$(document).ready(function() {

    const csrf_token = $("#csrf_token").val();
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    // Variable Globale
    let XLit = 0,
        XTot = 0,
        appendToResult = "",
        date = "",
        $this = $('#BtnImp');

    $("#idForm").submit(function(e) {
        e.preventDefault();
        e.stopPropagation();
        const $date = $("#input-daterange");
        const $ErrDate = $("#ErrDate span");
        $ErrDate.text("");
        const $classDate = $date.attr('class');
        if ($classDate === "form-control is-invalid") {
            $date.removeClass('form-control is-invalid').addClass('form-control');
        }
        $.ajax({
            url: "/chef/expenses/imprimer/list",
            type: 'post',
            contentType: "application/x-www-form-urlencoded;charset=utf-8",
            data: $("#idForm").serialize(),
            dataType: 'json',
            success: function(data, textStatus, xhr) {
                var status = xhr.status;
                $("#idForm").trigger("reset");
                if (status === 200) {
                    $("#load").show();
                    setTimeout(function() {
                        $("#myTable tbody").html("");
                        XLit = 0;
                        XTot = 0;
                        Data(data);
                        success("Données récupérées avec succès");
                        $("#load").hide();
                    }, 250);
                } else if (status === 201) {
                    let lgDate = 0;
                    let str = "";
                    if (data["data"].Dat) {
                        lgDate = data["data"].Dat.length;
                    }
                    for (var i = 0; i < lgDate; i++) {
                        str += data["data"].Dat[i] + "\n";
                        $date.removeClass('form-control').addClass('form-control is-invalid');
                    }
                    $ErrDate.append(str);
                }
            }
        });
    });

    $('#input-daterange').datepicker({
        todayBtn: 'linked',
        format: "yyyy-mm-dd",
        autoclose: true,
        endDate:currrent_date()
    });

    function Data(data) {
        if (JSON.stringify(data).length > 2) {
            $this.prop("disabled", false);
        } else {
            $this.prop("disabled", true);
        }
        $.each(data, function(i, d) {
            const x = d.length;
            let Tot = 0;
            appendToResult = "<tr>" + "<td class='bg-danger' rowspan=" + x + ">"
            $.each(d, function(i, d) {
                Tot += d.Amount;
                appendToResult = appendToResult.concat(d.Date + "</td>" +
                    "<td>" + d.Description + "</td>" +
                    "<td>" + d.category + "</td>" +
                    "<td>" + d.Amount + " TND" + "</td>" +
                    "</tr>"
                );
            });
            XTot += Number.parseFloat(Number.parseFloat(Tot).toFixed(3));
            appendToResult = appendToResult.concat(
                "<tr><td colspan='4'></td></tr>" +
                "<tr>" +
                "<td class='bg-dark' colspan='3'>Totale</td>" +
                "<td>" + Number.parseFloat(Tot).toFixed(3) + " TND" + "</td>" +
                "</tr>" +
                "<td colspan='4'></td>" +
                "</tr>");
            $('#myTable').append(appendToResult);
        });
        appendToResult = "";
        appendToResult = appendToResult.concat(
            "<tr>" +
            "<td colspan='2'></td>" +
            "<td class='font-weight-bold bg-dark'><u>Totale</u> :</td>" +
            "<td>" + Number.parseFloat(XTot).toFixed(3) + " TND</td>" +
            "</tr>");
        $('#myTable').append(appendToResult);
    }

    if (!window.Promise) window.Promise = {
        prototype: null
    };

    function generate(date) {
        if(!date){date = currrent_date();}
        const totalPagesExp = "{total_pages_count_string}";
        const pdfsize = 'a4';
        const pdf = new jsPDF('l', 'pt', pdfsize);
        const pageContent = function (data) {

            var logo = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAADDCAYAAAAFrxrZAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA3hpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTExIDc5LjE1ODMyNSwgMjAxNS8wOS8xMC0wMToxMDoyMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0iREM4RDk5NTBERjIwNDZCNTUxQTlGQjM4OTBCMTJBNTIiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6RDA3RDQ2Njk5QzgxMTFFN0JCNzZDOTAzRjZFQUIwQjkiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6RDA3RDQ2Njg5QzgxMTFFN0JCNzZDOTAzRjZFQUIwQjkiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTQgKFdpbmRvd3MpIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6YTQ3MDkxNTctZjgyMy1kNjRlLWE4Y2QtNWYwYzg3NzAwMWEzIiBzdFJlZjpkb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6MDI3ODI5ODctN2I1NS0xMWU3LWE4MmYtODg5MWI3YWQ5MzFjIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+IwtYPQAARelJREFUeNrsXQeAFFXS/jpN3tmcI0sOCqJIEEGMiKcYMCDmiHqGM4cz/Hp65uyhp556Kp56JsJhAIyYIypIhoXNeSdPp7/e61lYYBdYgu5Cl9c3y0xPd0/396rqq1evSvjmm28giiKysrIwffp0zJ49G9nZ2fj000+x7777lvj9/pP322+/o5KTk4ew/QRBgGmasMWW9oThQ9d1BAKBn+fNmzdjxYoV/z3kkENWMMx4vV7k5eWhtLQUAwcORDAYhNz2yw6HA+vWrUM4HB4yefLke84+++zDi4uLQSC076wtnZVRF1xwwahly5bdPX/+/I9ffvnlG4YPH/4FA6FhGOt34gBkiE1LS0NZWRlkWb7moYceunf06NH2LbRlh8Tj8WDw4MFsG7vXXnt9/vrrr9++cOHCW0844YT1IBSZamTgmzVrFlOfT8+dO7cN+FTaNMA0yOzq4Ja3dbPFlk3E4IgxEjiJ0xu06RZYDj30UNx+++23kHX9z8qVK5GamspdOZF8O4RCIXzwwQc3XXzxxecVFhZuOCD/MilJQaRNoo3ea91gb/a28UawgAIRJseIA6boYHAkEGp8B8Yt7rjjjpOXL19+d21tLfLz8yF89913ePXVV4cdd9xxX48YMaINmtkhRQ5CveVFyOHlELQwvasSHo2EGhTsYW+LJUztMYIqJMEQnTCdRZDSjqH30iHQZxJ0+tuiHL/88gvuvffew4YMGTJXZiyYtN4LFvgYqMjUktYTCHxq6FNoa86FI7iMHZt/LNq32pYOQWjpJFmwLG+8uj8chU9CSBqDtsgZNGgQ2/45Z86cUpkISI9x48b1tz6Kc7tsElK16DcILxuDZNKegpNUqajRsemoTL8KthNoSzvYI2zw/wgfIvEGMbwY8aVjofT9HKJv5Eb7ExHpQURkiFxZWXkmiwFaotCXRTLZYeirjrXA5yDlSQcUTMkiJPxstum1ZZP4XxsocmvMbKhbgTsUR3zV0dAGLIIsZa3fq6CgAA0NDX8WCXxnZGZmbqAxjMm0vAK5oYLAJ0AXmTHW6XC67fPZsu2MmHw2QVWgux3QI/VA7esbgif0h9PpRFFR8X5yUlJSj/XvixbAnJHFnPzyg5Aq5bTXNru2dEYjmoyQRLg5dnLvbqHFMAyDfESBK7OiokKXSHY4sJki1aw/uU23jLt9R23pvFfIXDdDsOiHGUq8L6I1kExmOFcUBGETVxIWnbbvoC07yTO0sBTbDGfRaFQS23cl46161L6HtuwkUTjsJEZSNnAJo4Ownm7fL1t2skWWEypu4wkMcWuk2hZbdppP2I7YExu2/KFiA9CW7gtAAQYEB22Swf/eoGbNDgjMhlwuoe2/BeuVxxw3Z/Kw8792X5G3z5oTWBhPcfvAo4yuCOCVCFRxCyzssyhBTDM25Oq0xVACnCxGhBj9HSPXVJShShIkQ+VgNgUr84FBW9AViILGz2v7p3s8AK0cQSFVRvU6EWdflwNPqol9BzqQmV6HZGcEfq8bmWlxZCXH4HYLUAikDjalx3IZTEKVqNJrHJIgQ8kgEBcFIYRVKFHaIWJaUSDGmgzZAqukw+SE3bCf2B4PQJOAxJRQVhwL5rgw53MGjCjemK0RsPykn9xQZAl+wlWSS4DLZUBxaZAVGSaPAhGeCEeySv8nGsjJc2LikVnYd1AFslwqcrLp4Pk6BLdEQKTXVfQNzYShCHxmpn1zbNrsvTvyYtPcDgAyjcS0mErg4kiMITvXhNfJTG6Uu5U6VGi6gWjMQCTE5v/A0xlE0nx1zbqlybwupMoaflgUxDtz/chIS0OKT0FRnohexXHkF4jomQ+cOK4SDq9B32Xn1TeYc7V1PNB5WaYOz4fUEkFOG4hdWhKPh83CyduDP/aYxWoBE6a04NEyL/7vaTeCBDG/wj5RIHGwkZlWWhO1RcTJ33OSif3L5UCAAPP2jBhaYi5k+FmeDQGVANUUjGHdTyLmf6ny7x0zxospZ5qIlGlwO5MAD0MyIdpJgEtycB9RaCb/M0DnVUUYpiPx21QbhF1a9W14PNuhAckUihI0TcTSzz0YPjaEIbOS8P3qENQ0Ap/O/DZ9k4i3DgdpzbJGF0p66Tj1zzrGDVRw3F8VUsNheB0q3A6JNpDptiZsKmpM5PQgXRpLw+rVflx6lxNr6p0oLYkiTdZRUpyEoYOCGDHEQCHzIYsDEOoIeHVEVSQbfLutD8jYqZSiobbMg72OKOEmGEodclOTCTZkgqU4sVs5wZVbiQOpWklFdo6Oy/7qxZMv65AUExmeRsi6SCB0wqLVG0IzBTlRvPiahI/fT8YlUwN44P4M3HxrI2bOZ8d0gTEVpjt7FHlQlOvB4cNzcMn59fAPDkMoj8CsAZt+XB/uMe2Q524SB2R5XkENaUktmP10Oe6/WsRxB/vIBEpYuZptCmrCzC2z2K6oO6GLOsKSAg+ZZL83jO9+0fHzzzF4DSIlkgRjs5ihwEGZnwWUNTXhsltlTPtXA2a8FMHcl2JwMhbuiKFPLxNNZLs//iGGGx81MOLYNFxzWS4C9ckQ9iVv0GkSf5EJpu5EFrfNoneLOCCiEhyygQnH12GCL4Crml1Y9pOEz79U8M2yJMz8SMXKVRIyc3WkuwIETh8kAqPGTkf/y0kVuGqKIpFv2A4wTJMxZh352TL5diaeeiGMjz9z46P3RKz8sRYjD0/GkuUa+vYQkOLRScNqKK8F7n9CwzvvpuO2K5Jw6pQGej8OY5UBTXRw9i0K0bbZGLZ0Ow3Iv0UmzSD7Vk6vvzG/qxG996rDmX9pxuP/XIcFrwTx1wvIODc5UdvkhiCrfGne+kScRA6isMVV7pYPyRfQmwb69nZi5UryC3vFsa5SxJplBvr1F7BkFdEeRsp1E5lpOvqWKlhdaWLKpck47axMLP0lBeJA2ieZTLYZ5dRfaDtjs9H57FX33QOA3F9jwWFSZ6IGQ3PAqHJBW6nCWBJFQWkt7nhqLf5+TQT1jSZatDBpHiIohsIhaIhqp3m7HtNR0FNHUrKE4UcKmDcrgsXfRtAzD1hSJhExJm2qKYgTEItzQigpCuDlGQ4MOzwN/7iLzHLUA2GACCGXDudgC2cMyy8UrFCOybk7/ceOYyvILg5AM0EuGBANEaKh0UOLQzI1S8NV0bY8houvrcd1pztQsy4LDcEgkQIVikHaSHN2Us8wwMgw4xKy0iVkpztw6BQJH70hYfmvAWSlmlhdbkAmt4BN2xmal+BkoE+PKCRnHJfcquOAI1Mx7c7+WLYkE/D4IPb1Qywhtp5mQPTrEHPoND3SEBM8PJxpg7Ar+4Cb85KNIox8cVOzzJMU7p5WDm9aJm591I/6hji8qQay3ZbWISwiGhWhkEZyOQwytx3PaJhC4l1NhdfvRDIRmHFnNGH5VyJ+mqOhcJgDtZE40p0a9zVZjN3QTKQnmaQ1PVhZbeDi2zVkP5qEYUNdGDvagf0HepCTY8AryVi2LorZM/0Y0s+PU04vB1pisJOFfgcACrtkqJNJUzToTQ7IehQ3/60cJxyZg6df9WLmhwKqKsKIkOaUiYHkZKtoJjMddYrISFYQ040tLgFlptIwY8hNJh8znoyBBwYRrdXxn8dimHSpgpRSg0/dcWrDZ0kE0rhRZGXQNaULCEeAWZ+YmDWfOZcs/OOjfTz0GsAl57Zg7BFhSLpGGtdWgb8LAFVV3TVHpocvMgYapNdVGgbsW4aHDnTill89+GmRgpYwaR7CSZ99I1j4kxcnX+pHDZGEtBTSjLq0RXIiGQJUAkhBto4VqxSMGx/Bh+8ZOOFtB96YZ3JmrPLCSqKlOkXi28xtkCJITfYi2+umARCh65MwoDiOoUObcfwhjRg4lkBZFYXRRJ6qbGu/bg1AK7wiWBggEBjEXEVTR2pmCw6ayAqIWBWTEBJROFzHo9Uyzr1FQoqHhWqMLZJRzqUFyxz36kG+4BdOPP1oDK89EkTS3j40Rww+N81KynGSYXp5KAdxE146fu8+yXwG5dijIygZzeavawACnbbUCVGRCZi6zYV/LxIi/C7etsBDHxw4TS6Yq53QVnihlrmh1ZFJXRrFOdc34JTDHFhZTiZT3rbHz47HKn+xDJoL/+qF6Jbx+F0qqqokSJLQJvWViIbAcgydqAsAPyyqwfQ5IVx8i4abpnox/WGi0vU+yANoP90OV3d9Frw9JyLSILI0BjkEUwrxgLCoixYwww4gEMNjdwWQn+1Eeb0ExdS2SQsJdMxkt5WqeunNJs46GsjPNNEcjCcW10vrY4rMBCukeaOihHX1Xnz+hQ93PaVhyl9kDDs+B1/MSgOKJDK/ViUIwfYDdx8Amq2pUkQ+mD8mkp6RhBAHpcCKGa52IGO/Jtw6NYRgE4FGdCbS/IWtHNeErnpRWCLg8ekmVi43ce8NEVTXeKCgLaER4DBkOKQg9KiBxnoPApoIK31bx7cLVYyalI533siA0MPkdU00mQVz5MR12NJlwzDbaoY38+MsB41eIvSwnVDKIjj1mHI88GIpKsk0Z6ZG+ZTcFgHI5nqJ7HiYLRaT8ejbDbjhHBFuIhFhcm8VxeSAZyCKywrKm9KR7Y7jgL1DyEiNIC9LIlCmoSEQxKwvIjj2fD+W9YqjV+96CPWkmQXVrga2ewCwIwSJPIXVlIgM1Crw7mPi3MmNuPZOmQDoAraqBU2uXdmUXVFeFNNeTsd5J4Rx1Zkt+NuzHhSXqsR3SEuSCxBo1HDsWAG3XRdF7/2b6KsxMv3sEHV0GgI6se8rL0/Fm+/IuPZvbkjVcR5OsjNpdgMTvCW6bAoiTxQwHXEOiHG9iYggBaqBrZpgnu5KGkoTBbhI66nxKL76MYZzpqhWyEaVLfpD51F8MtYQ4f3rPSZuuCIDlQv9QAoLmpP2rAkRCFvw4D2NOOtE+ntVFIbMUmUlO3Vhtwbgej1maUNU6hg6OoQRQ3XU1GCbE5t5VIYAm+TV8fpcN4FRR59SDZEIuAZjZN/vMLF8bQv+O8+Nu6e5MfCIFNx6fQmBMAlIp++z8+ktyMqgL8UkvmZFgJ2esEcAcD2M6NmLRTGcdGIzorHOPX1GSHLSJLz/kRNLViXj+ENUVDWIkHmBbI33pkiWHCjNMAicTXytyu0PiDjv4mRyFlMhp5EzEJFgEknRnay0mMK1qw3BXQQ+UexqAGRLME1uhsfsrcLrdUDVOvGDTObKWSGX75dpOGykCNNwcR+R1SzWZBkRIiKVTQEsXZmCFmZ6EcWzrws4/2JSgSleuimSFTc0rR4p5jYwcVu2U91sz6KkXQ1Aw3RCbIqjT34EfXJFLCezmJmyrQvSTTLDDriTQvjyWwPjR3nInDYhoCtIgoMvgnf4BEwc74aiR5GVFUGGX0OoJRmf/ibjmzkpGHZgFYwmZn3tGol7BgvexI8zRGLEQcBVbODgAxrxwwsuZKXK1rTaVuEnEGVQkZ2k4P0Fblx9fgBHH2DiuVki/PkqJDGA+ion9h+chctvWm1lvDjYImVi4BUCqte6oTaJUAzNzpreE31A9tBFU7NcLknFEQQeUWHdFxVY/UuErR6BZcuIBKrmQAwLvoxj6jmZMHQCrxmFJKchLibhnvsiqPqCfrqDgLeINOOv9NVABNlpDbw0iA2+PZaEJPQge/5hE70LNGT5nYjqjQyRELZ6uSZfzKST75adquGfr6Vhv0EVOP5QF5at9fP1IdkZKlrMOEYem4HfPssF+sbJyyONp9NJVdGGng3AhLQARUUtKMmLornZzQG4dTZKrEoMkf/mgDfFhd/WmHj4CReeuyPOk2MbQqwsSBR5mSGsrjEx4aQU1CzPgjiY9UMh8GqwGa8NwISwcEyxibFDRETCbmumZKtzsgI31SyJwDBE5OeF8ZcHPYiTWZ3xjxiqazXE2VqQWAb6945jTbgJvYcm4bJze6KuKQlCKiv/odi1sW0AWjmEbH7tiIMb4VFUIC5bdWC2FsbhANIgGzE4nS44U2IYfJQPBw124t93iSgrk1HTGEFjgx+HD8/Cg4/WoFdGPV8eAM2RWKBkA9DWgAxsmonsPDdcbgm6qmwzleHLOVnreENAfz8R3FALBk+SMGqgB3P+7UDvHjFU1Tfi3U8CWLPUgcuuDyGrKAAEdV7gyFp0ZW60CZudw+xAB2/6mQ3mbhOG2ehBsiwZp4Q577vR0BKBP5UVtJQ6ERNmUfYYuZIO9M/3YlV1BL2PM/DCvTKe/YeAL7+WsK4iDr/gRPUPQHaxCEPRuAbleYBCIo2LwMghJVgr/vh1tbaEdOqt+a7re3vrdD5BMCxXgKWe2Rq1ewIQHhP6Ghn/fS8Il8fLM2bExLzENgd12FJOAkOMgFCUbaAlIuOMq33Yt28L/nKegMumiMjsUwcw4MXoHLEweJkuHYkULOYG0HFYmrQDVkkap4c+oz+aVZ5Eq8ZYAU4CWDJdWaoHEpu6aSAHNizzwJEpmqy+pi3dDoA+oOx7J8pqWLFLukzdSQ8zmGDDndGk4CpKMxT4nAJKejZhZQ1w2jVe+JMM9OqhYMSQdOw/UEWfPiIKszzIUHTILDgtEmkRJMQ1L8JhJyrqmvHbCgU/L07F8jVxNNTTINEESLKOtHQFA3sCI4bGMHJIKlJLqiB5CZQVZM7DRmIdix3k6T4AJJevJqigOe5BqjsGlqDVWfBtqhENnp4lIMWv0BaFHjOxYmU6vl8Yxz/oDP7kDKSn+5Hs0qA4whCkGPEgBTHSjuGYgaZ6EQ1NTK9FIUsKHC4CH12SqkrQSBO+OZc0qOhCr55uDChy4IwJKk44ht7r3QKhQoMRIJMsJypd21a5iwOQrqyxxYNoxAnZG+a8gKdV7ZA/JfJqqiJrzC3GoSguZKWQ/5fKdKQT8TgQaqxHnWkRGAZ4tjZFEupJywlEhhwo9ssQmX9oqpsQDZGDTzM01NY3Y8YyL2bPk9H3Xw5ccIIDl/85BDEzAHMFS/NSyNWMkptpJ7p2XQCyAvrkjxmaAUHYWWV3jUR2PSuArnD/UCMgWm+S2SVfzucEklpBzhvES9gQBOcNRxPEVtgk/sgOr7OW38jwSsj0h4nEC1i5VMEVt3vx5v8kPHGPD4PGNkL4NUq/i/xTUd/jFz513SHIMrNk2arIuisOnqAzVpv5VggJiUBKIpgibDnk0tGRrRCmyNPDCnJN9CiN45NvnRh5hB+zX8oD+vvoM7vlRNcGICma1GQNbhergiAmontmt7u9OqtHqAvoXeokyAfwp7NMLJiVDPQjmPNVeUKbzQZg1xFysXLIjCU7mxHTHQQ9B8RuB0AWCnJAYj6lHkBRoRuMtZx4gYKGRSkQ8hONfPZgTdh1ARgCCgtjyMvUEQha63d5Z6VuJ+b69S4x3US/IhWVdSImX+YHnDIEr55oSdaRqTdtAP4hEgQcfQ2MP9CNSNCAg8iCIXZnTSHw2RS2fLmkUMD7CyQ891Aa0FuCoGhEhkTeHcriN8Z6o2w199k9NaTD4ejCyQiM+QY1XHhcECl+B1oiLqvcWjcWZoo1NosnqchMjeG8v6fgxScKgZ4OyKUEOK/Ka9jA9PKCSmxRvsDBuHtqQUmSuviK62oBhSOCGDu0BVXVrIKBnjBo3TN+1sp7DXIlUtNEpDuDOPcyJyZOzMOsl9Np0GUDRckQesVpi0HIVSGwqq+JOtnro9dmolPp+onJ7lnbevtadf1uBou1+JJJa8Rx0yUG3v0yipaAAJ+LmKUYtdKuIHZbH8nUJaSma6gNhDDjPSdtMkaOTMEgAl5+SiP6lIgYMlDgeYsoDkEQDauKQ5PBcyV1w8WbOArE1kRDTJj47ncv5K47OsCzmM11BoadEMBls1Jw3wsG+vUIweDNbRSrbks39Y9CURMenwP3XBtEeYuIN2cl4YsvArSxzIV0MN6fkmlicB8D+w0uRN+iAPmOtRi1txtKnxgNTHKS69h0EUvTUGBKGo8tdrfAdtedCeE9RMg5Nz1QykO4+eZqzJmfhV9WudGnlNUFjLYpm/F7jPydGzgOhASkZRq49kpSZ9lBXH56Gl55R8L785z45LsW6E4/dEcMX34XxAcL2Lk98LqyMIAAedhoP/bqLWLMXk7kDSeaItYC5XSFQcFaV73+ekUbgNuPP9YUW4Iuk6NaLSNpYCNenAaMmJiFsmoNJVn0mUasUhQsZ32nglBY71fx0r7cvLW+p+8cIJK2Yj3y1CoVSqOO0pIK3PR3GTeWZ+OR50X863UNP/+s8MX5fYqYpo8iZLjx02oR3ywE15L55DIef6RMm4ax+9GAHRAC1sZgBNh8s8xrJwqJvMauyqTFrqwBWS6dwwxAcBD5WCxhyFEhvPtsENGQjIomE06TtfmiGy7szNVsVsIC75ptWv1D2JyxwbL7hJ2nBTUCoEch9ut0MloMs4Z0wU/k08XLccXVdVg4swFP3Koiw5+JpWUyIuR2eOQYCpOB0iKTAGsiqpl47HnSiKekYOhkH156KoeuNwlifwWih5WJYKzbCV2QuiyT7vI6WjStOVWDlcz4VcdBZ9Zi+iNESBqdNNgNyGYyZMPciVnHBq9XSF4/NxBB1UAgbnBtwopp7jQAahJcDiIXSognMbBwC297TGbUXEbg12O4+KYy/PZBBc49Tsfach+qa3xwy2GLDdNvTvGq6FUSRn6+hsXf6zj9cg0Dj0/HjOdygWQCXX+6Py7Wr6/r5mR3eQC2Bhh4VnLcDSzSMXlqOb6YriJcS5qwPg5Fbttpc0sHa9VurbEMY33tSWvNscC1XXNAxso1rF51EFJcgxJyoqyMtQMTyN/aOY9Si5tWoq2brX0ReIk6fh30T520Vpx8RPzshSsjgGdeCuCdx0OQZZN8YA8v9i6ysnasF4rBchJVFOa6STNKWLLYxKSLRYydkIvnHywi1zEZwkAyxxms2JJhsbvWgbbeMJvY0AncBmD7hISnxzDNYEJf5EFaRgvefyEO0XBhBStsrrCwjEJWR98Yvq3Vrbi5ZsWL4okjOqzqqvRQmoMSVpPvtJJM3ao1HviSnLj0HAkvPyzi3eejeG9mLW4+H6isYe0d6CymkQBrJ/1K3keZLS0gk2uqGFCaRJqKZXvriY6hlq/GOk4pCPPfa1TS2+uCOOaianw3pxEnHmFgeZkDNY20p8PJZ09YHezWuv598k3SiDo+WWjg7JtEHDwpG3fflI7KFSnAABeEUnJX3KyXisLn1zUiLYbA0tNcicH5+4JQRncRhiGoEOiGCckxnDU1BYftD9QviKDneBFLVgTQu2cazBgBUQpybcfKqzkcGqoaVDQ2MYZoWJVQOYDYOmM/+WECCgqCOPggCQfsFUFJmoz9h4aRu0/U8gPD7C7FMGisQL6YC9Pfc6BvTx2SGoZqujrhW1mDgPtlYoxuvA9DB9VZ52CJqYpuva7fV7QWQrHVfRE6y89EvPaqx2v/iWPa00n4v7tp4C0PoqBEgSI4yMzGeMJujP1uuke988A70S/4PowPv3Tg8df8OHpMAw7fT8Nxx9A+Q4MQmqMQGcA1FXFZ5qXoZPP3hWD3AWCrFiHHW8yME/g03P5YMvqWNGHtpxJ6HwIsWxFEv55OniLPbj+5WQi2qBi+t4h+/VREWsiflA2kpmjITCLA5sSw12A3ivqSb+dlDeIa6WsE4CYCxQoyuWQK2WokmXVv0kO47xYRH3yTjtXVBNQMcvR5d/h4G+a8VVrFfctgWEFxjgdD+6u8P4kpMgAx/3JTH1NYb6cE+p62inw6TzMuuiaI8Qck45pb0/DGXDqmtwG9soh8qE4rSM/0bELzF+SwhkEmmghsT77opk3EuFclHH2ogX3pXo0Z5gX61cOh07U0Gvx6aGSx4n2bOkHrowPCJkEpM7E0UNgOtt3NANgKQhGDWaNBUk9TrnJDVkwsnedCyWgyo1UhFGXRg9DckIghV5OSGT0SuOnuZiBE6sxLAIuQOWpkrSFqsWJtEv7xWDrGDA1h0P5k3htI8xDhYVpEYk0YyRwaTDuUacgbFsQrj/lw6BQfmuU4/ClRMuFiouumvhUTxrxMlQfQA6TR+vWvQV4a7R8W+EJ61j0AHbBsPuVmSLz2lx6m3/2jjh59G/Hft0y8/KwX9z+Shx9X6UjLjCDTI0EzmLuhrU+yNQ0VyV4JyT43+ZcqPv9Ow4efp0Mk6zB8sIzxY9PRv8c6DKeBWLQXwSiZLEjAsIxEhK4rIvPezSafEyT3wbCWRuiiyLN4WC1FA176CXGruFQnQNjtAMhGmKDpUDwyJMWBrHQVJ18mI+2pRsye5sLgSWkIxkNwyhqcrOAQnKisYA+W2GbIh7uuK8bcr6Ooaw6hvqkXqmpMHtD++Bnal3w/vYV0nqavv8ks9CIacd7G1VwZxyFHBvCPW924+P9McqPYAicNZjSJd4dnq+g6cgw5D2XZLrRfLCogK5Vl3NKDbmbva4lnJnYQEt3Q7d3ajUBfRhrH1YgpU6OYfEwYV9/jxZPPJWNJbQtp1zjcDg9iQpwDxDAdiZpPYZ4QUZBtmXeN/N8fflbxxTcGP3dxZgb2H+bAwQeEMLSvgJyUOuTlKJDJrxQ8BGiNLV+FFQslX1xysBVZtFU5ufsg8ELfu70GtJ6CKFpzwW76BZLHxJ/vTMVvi+rwt6t13HifF6UlAaiiD2wxb4rSgGCzBzOfy8JNTxi89FtWkgeqW+SVsS47zcSY4wkIaw3yp7T1JUDMNmaQFzr3AL/MdWBkPx2zngb+dL4TUVVEdmqEHoSS8FM7ZnsaOfuCTANB9+HAfQiwGazZt7hdkR2BQKgTCIxFNBgzmvDgowGcf2wEtzyZjLdmkgY0Yiguloi1M5fXSFxXm5ReYtI0hJGfSWREDNA+qQjEDLz+vzhtLiQnR5CclI/CrChpRxmDeikoKW5GKr3vFmUEtTh+WyciRU7BkeOakMLyGqNefqzdWgOuD2Pw2J/GfR097MQZU+jBeptwzkQJD0zzIRr2QWZ+He2VmePGiw/5SGvF0LOHwP19ts63pjKCYw904pH7yslZDPNWD6LAQCnyuN9GN5L92Syix35hTL7QiYun6Phllokhx0RRFjbQM1dHVLRMpWSwBfGbz1Nr9Hm4yY0+xcD5ZzYBDQJn5qyCP6ui0JlkApN/R4Ko0PXWOyE2xNB/ZB1eHxPGR7PScP0DKfiKNL1ATLqowOD55Hpisb3Ayziw8+mcBJlGEikyDX5XHKkFMvnOdJ1E5mrJbyxbJxORkROkjQ16GtSSFxkpMg7ZP4QzTwnA6Y7zFhcakTWpkz19uicARRaTY5PwrBIgPXClhVgfceSWYjS1eJGd1YJKIhwpupNGq4GqehPFWZaZicWDWFFu3dArzxXwwF219AwiMOmFRSPMVp9rE/Dw7Bwy6d4iYsz7pePIsxTMfD6M8K9uHHSKE5//VIeCXCd8ioG4EEvcWrONCSYCYTjJ/AJZxSKamrLg7V1N5j0KrcYFRj9lM9YJJ17gLqNImo5F6vlzX00kS4jgoCOr8eXYAGa858Kj01Iw70v2oYr87Di8TgKK6WYNAEhbxXj8kdXDYVVhOXkhBDHNmuxzYECpF1n+CNJoy0hX0KPQhXzSts7kevTKNZDfj/1G8qsr4zy7R2QNKDsZ2eu2iXWcIOgeSJKO/FwTdz+m4ICRLhw1VUGESEqqR4RTIx8tTcBnXxlkPhqR4najsjIVk491YM7LYTzwIGm+WBBancIBsDHra2eORKIbvlrCeSe2IDNbxtFnybj3GQ2z/h3GM3c7UF2p4Lcy0jWy3k4RBCIhpLXzMkQsrajHvsd4MfXcVNSU+yH3ZZkssQ0x4m22w0ZiBZ/IKQ5vj8yufjkrG9KCY06sxtz/VOKt54I480Qdjc1+LC0TiZjpiJMZkAQHL18CPssjJOBgHYS96yIyFje8qA+5UUsMedkKJ+nLNIwdH0F+KfmvlWQ1yg3Lv2WpYWbn4dQ9NSBZjjRflEyHn0azwTNrF1fJiLSw0h3EduFBQT6ZA6cAlyLjsx9dMDQC3cwaxMtFjDmGfDYnaY4VpDkIrJK49VVp7MGycIzaosC3VzMev07CyVem468PRDD3Yw23Xinhx3nAIy/q+OfzSXA4wijKB2e3LB4nGG7epNEgM5jscaM+2IKnXnTj7f/58NJjIRw6uQFYRZq4gR6nIiZIQ6tT35m8R4EvY1YjNKiWmlBcLTj2FNqO9+Lij6P44KskzH5fJ+Jh7et1a0hLZ8m+5P/KEmrIWjQ2MdMcwZKyOHrkxtGnjw/5pBHTU5qRk0a3v4qYsKpz1i6zmt47oMe6JwAbgSGjIjhgbx0LFnohO1S6iTHsXerG/vuqSJVb8M/XPWghwPidAvdz3nxfwjMXNlpOP/k1Rlzm1bBEIiSCoW8DebN8J4FN+xFZOWmShkdJi361UMQ3v4kYd6qM6y8xcclJJvbtHcVzr3jx5S8mrxtTmEeYYCyZfEOdTJ6oGUgnvymz1MSKMi+OPMOBuxe5cdWFHgj7BiDU6nx2hP1OI+Il1yvcyVIe5OcaKplTIiNRBcIishaOEPYfRduEelx1jgezZvvx6fcKvlui4Nvv4uSauLiPt9+AAE6+SkORK4Z+/d10T2mgZpN/4khkAtWTma6XeUVZgYeVxO2uMxKPE0ufNm1ay9SpU5PazqSaZZfCrHocolvskgnHgkYXlSugZk0WXp3pRL98HaWlIdJ6pNhKWDglgtvPz8Wtz8joVaQibKpkeoFv/h3DvuProK5zkT8W56lKnR29PDRD5xd6C1j8UR4GHCsijzSIxytg+WrWOlZD09oAL79x30PpmPmuiE+/ifMEh4wcH1KcRoKVitwvk0UXWkI6qmqjGD3aiwtODGJQQRBeKR19+pNGZMHxsLZdhY1YCMYaWG1CxmxRioc0awHDGxGKtQo++cxLVkLCV8vjGFjowF13koVIIo1cr1lZ2NFEwVAzMSUqtM7UbOOFROn3Zp0Gs+RFcp0MHmVgMzxfffVVQJowYcINw4YNc270heY5xAq/hqB0xRwyk7MFs8kBX14Thk8IoueAENIy6GEydldptVcadWAYc+cmYeEKkN+lo67ej8xcBQcfHYRYze6lbAWAOx0DYTEggc8YZA5TYdTkYPanInK8BnzJBKRGEaMHKigdUYsDRjTj7GNVlBQapGGSsXqtD5VVcWLwKpwOphVF3n7CQaYvI8WBxcui+O8sL155348HnvfAn25g1MRGCKzCltzWN93W/mXC5jMrIku+IU3cLECq07kfWbxfCw48lNj9sTEc1C+GUIUGOUJuQzOPHW2YBRHaHLMzt40pDO/eQMrxVkWIBAArKirioq53t+J1Ar9phosefiOZmN8IjGtopNfQyIrEoSsmtCoa3O4wZv+7Bjl+CZVlCj3gMF57P4DIQj8EVmCI1YTZztQqng3FvtsQx+2XV6FPSQSrQ2TmiKTIBKonXiRHqTodIIcfLc0467x6zHmlHJ+/WokbpkZQnOlHNQ2IFWUGVpNP2hQlc2lGUJAtoaBEQxIxVSf5bnf+XUPZlxnAAIMv1BdM72bsenuuvbXWosnq40QcMNdq0Eh7Y12cBkUQSWRBxJjxu5TwEgWhey72llkOHVsDwUMehrWxeiz0vkz+lrkOSO3djLeeaEALyz9xC1i2NAX/+4D2yw1jR3pQm1yRCLy9LHoGMeUIHWHSiHQzSduZeHuujvPPJ/OWxEyVEyaRHdSGMXCfatx1fzO++m8F5v27HnddL+GwkTEkOUSsXOvCqkoDTtbVyREgAqOiSfPi+HNSCOgZEPKtqeIdXfLR+n1eNFMkU0v+MjOnspFwDdg5DD1RIfZ3iah1T9kQL2tbXyXhpbFBxfLrVgIjTm3CpZNZiETmTvbna8j2seRWQ96hszOqyZNXQnGcf3IcBWkuBKLEOtnUA5GepWXgfiC/DrbRzgaZUm1lHJ7UZhxwWBVuuKkGc15qxGfTW/DKsyJGDPZhxVodaxoMYtxuFJeo+G5ZBGee6+fThEiNJUzijmsms3XqLxE6MTeqUfP71arZbQvUsdkFnSUHrDNx/83lGNiLjegg5n/rh7mcTFlabActjMHbuaJCQe6AZowaQUqOfKrqJh1ZaU48fVeczw2bsVjrTDB3n1gPOqOFGPhaE8aKGCcY+b2acMrpK7HgtXV4/lGQic7C4tUOSBETpcUi/v0+8Perc4AShYhhnM+27C5V3XZbAPK2XyxruIac/J4x3HBenP/cH7+N4KU36WdnOHdAkySKZvDZAzqGK47CjBgMzYmGegMXkkbsM4FY5Dqm+OSNtAnzvwRYQVs2SAxN4w3b8SNdkxbEmZeuw5fvrsXlZ0axvNKB+iYRJQUqbpzmxpN3ZAP9nDyhlLFZVvjIBmBX1oIGq3xPWnCZgiknNWPMPnEOmLe/TLOSB+Tth/f6xUuMScsK3E4WBI+hV0EaLruwBlijW9ZtEzW7cVgEFhBZhI1ApbHyI98KSE6tx8PPVOGpe2NQowrW1UaRkaXjottceOSmXPI73RDyWKxQ22jmxjpV96qSsPvXiCW7Z4SJdBQEMelIcrqRhI8XOLFkAaEvp7WFgrldIOTJAyzQHfLhl+Uu/u5fJlcjY3AYRr3M8SlzLWlsXVuzJB0zDlEmP7HCAyyN44Iry7FgZjN6pbpQV1uPjAwVV9zlxl+mpiEayQIGkSZ0W3UG2bUYbCE/X9nUfSpG7NYAZNkeopXiAtSZOPEQoCjLQH1zHLc9TY69i0Aoy7zBYWdnGgTT4DMNyJDx7ONOvP2hF8P7J+HcM1Rgtc47cbJ9TFPcNoc+UanVlCKQpDBMlf71q4YhB9Tg2w9VHDYiBXX0G4oyo3j4WQf2OSgJbzxdBHjdQK8ExmUHBMVKGrWWqpo2AP/wmCESqfD1pPD2UjFqf42byrc/8GHZF2kQWXhD7+wCIz4zDJkBO27grfeZP+nEuWe2wDlQ5WlWVgFyc9tjacKGOoJITG8x8JpLBHgzq/D+7CZMnqCjrJYGUb6J8poYJv1ZwD6HFGL+zFSIhS6IyT4Ifj//Lbx0iQ3ALiRMMbjDGNQzzMFiRJpwzs1unp4vZkVhNYvrTC1oRj4IbOEklMclnjjQL7cJaA6RKXTunCCuVagfBgsdResx/ZV6XH6OhLJyDampCnoW6/jxNxlTr0hDS00mzrrEh1f/64Y4iGULxduEqkwbgH+4OWZpR5KG9DSdxwP75QGffSnh/EtZOj2ZYBfLqbN6kWxTYgKL2GYqeOQZH378Ic6PXdPC+j04SIFpO5HNs2k4IjRVAisog4f/sRa3X2KirMKBUFRCz56NiDrDOGqSiBfeUnHWTQ4sfS8XwhAndPrNqqDwpQCwKyP84ZSYB4ML/SwbOIyAlETM0sSz/xWxhpgnC29IHtJjutV1fav+E2Gt7qckPPC0AiVJ5oXIPSx9JdUgZSrutCpV1jozGjQSHa+arqkqhpvvb8TdV0VQVa1hxQod4biCr1c6UFIi8s5NY05OwaczsiHnyqQJTXQ+0dAG4K6xwRUyDpsIHH2AglVlOpK8TfAnRbEylItZL/pRUylC9LitedKtHY4U58pVKiqaHfB5XSjMDEHxZiK0Khmyou/kWn2JdSnEkI0memRro7ju5kq89S8nJv8pBW6DZVs7sHaNB2rcRDVpyjETfVj4SxKkXG07ky5+H5H3HACSaQ0ZcBQG8NKzBk6f6se7n2eiZ34Qj7zoxjtzvHhnWi2O2b8G5m9GojZMx1oJARElPcgKk0kPtmjw5YRx5CVZuHiSD4/cT75gTWL9+851JFjRRBghMszlBo6dvAbHHu3Bmm8kVDfVEEt24fuVLsTjQagREZk6m2lxk08a4WEeG4B/rBfIa+eZawz4S5vxzhsG+uyfhDXrHKhuIGqJZCz4zoNjzrbqMm9VfxHGsoZEcMWpEVz/gAMxU4IW0aGz4DArfbFLrJ5gZUkzosxSnBbrEJRmFA8BilkYUo5gAuvsxJe/GHwa0mxgi/FtFtx1hKW7r6FXbxB3nFePcIzMpZmKzJwQnn1Fx+J3s4B8bNFv4uySPeSGOK69qBn9igWsrfTBJztx1pFhzqjNXT5Zy1LvRb5+2aylbS1tq1gChmHFIVfSdcbFLq9i9shueSYrakkgPPm0IK64gLW1NlFbJ6M+JOKZ10iDeB18nnYLITto9GC1RhlCbhg3nR8lk+fFweNC2O+oCGkeBTuU77VDet5apNRdWjvsoe0a6SEFCWhaCA/d04DFM5rw+kMGRg5z4u3PZTT9TADyta512ByIPB+Qd1WnzyoMnHZhBGP2VnHQUAKfT7UW7Nh94LYqLBla3jN/Olt3KEBrFiCHW1DUh7aRMiZN9OL7L0l3RONAnNV56Yg9mtYySHYTWRU1uRFzn2N4DMNgK+0kCbKpwW4JvLXHYO6pALQKArGKU4YuQG9gGcsGFCWAoQeavHCRGTW20B97Q60Wtj5Fa6bvpjcSaB3Qgknk9IdscG3TYxD2VABumCljvFLSrNVepkoar0awNJ+IreS/J7wslkTAgNxirRwTWcgD2g6tld2TRN6Dh19itkPjyTLmRi6xsQ0+nJAAsbbeMbToDBIZMLbYANxWQtKuie2EOV+vE23g2SzYFhuAtthiA9AWG4C22GID0BYbgLbYYgPQFhuAtthiA9CWLiXtzoSwBTU8H1MwYad02LJzpDU/UugYgKwps0T/qWo9eNk90UafLTsuZpTl/lUm8jvURJVVZXMAWg2ZRZhpk+glBaay+5QBs+UPBKAWheA9kK+lZgAU4G5fA1oJwCocaccRCI/DzmtQb8ueLK3lLjWT1fGWE31N2vUBHYnmJ0HezFiEw757tuw0D1AQlERDUKtrlbBZQqpgFSMR4LM1ny07VcTEZhXYFxNwE+wwjC1/PDBtseUPk3bjgC8+/wLuue9eFOTm2WFAW3ZYampqMGToUDz3/HPbBsDVq1fj10WLsGLJUhuAtuywxHQNcU3ddg3o9/v5a15+vn33bNlhqSgvR3Z2tu0D2vLHSdtKJ6YNQFt+dwDaLNiWbsOCbfnjxeykJrEBaMtOBZ+5HebMBuAuFlEUoWkampuaoBsGOuwbyXriigLcHg+8tJmm2eXDSaw8iGqYqDENGGw6lKViCla1P56SRP/TWWcIugdZifdFSUFjUyOCwSB9v/3K1uweJaekwOv1oiv2hpZNs/tE+mKxGLw+H0aPHo36hgZUVVdBaEcfsDlGgwBaUVGB5WtWozA3D26XC1oXbs4dIfAlSxLOkbyoNwNYKxhwGgp03vHI4L9Tod/VoKlYownwyQ4EA80YOnQoepSWYumSJYjF45vdB3Z7li5ZikAggKSkpC4HQllRlG4DQHbzdNKAyampuOPvd6GkpATRaHSzcc8aRzMNWVZWhldeeQUP3nc/1yiKQ+mSmpBrLt5ZyYDDGcTf5VQUCFHU0nsiFNKHMZ4q7GZaUnHjjJiOuToNRkNHjO7HiFGjMO2fT3V4/Pnz5mHyyacgHArB6XJ1Lc0vy93HCnvInMZJCz4x7R84+eST+XsuuqHuTTan0wmP241+ffvi/267DYcedhjKqiogiV2T9LOrcioSWkwZDwViOD8YIW3mhI8GkZt+rzOmQVE1mNEY0mnf0iQBcSOGXH8mvvn6a5x19ll4/l/PdXj8gw85BAV5eQiGul7dQrE7mWBmViUaML1KeuBruvFPPvnkNn3vyiv/wl/jqtpFf5nAl0MYioHeQjJptwD+I8aRZLgQkAQ0EjjDpNXDIuvSLiKiSpAMmcy2ymcYZHr/vvvu4/5xexIKBKHSZ0IXHIDdMg7IfRsSNQGorQ2hA8eMwVjaKqqruySDZNfPOholqazHcBSC5GZtSOjNGAzmTrAsYvIFGfhYbWrFsMy2aY1KJJNfzBpfM3ek3YFrmjwh1MQfVTp9NwNgc2Mjz9RpNcPbIuMOOZhPiItd1AwzohsnKqwR4ByGBA9HCnl+BB62iVabEw4jVSJtKZiJf1uWgbkdXfW37VYAZDe5pqmRs7+srKxt/t6JJ54EH/mQoVC462r2xMZ0m0ew/nKQznLR5iYQukwr9OSB1XzQQPcW5v51OwCahnXbp5x+2kYPbmsyoH9/HDn+SFTWVpO2Ebp0A1NdiGCdTr9KToKgiAQ+EaZs8v7aUfL3KuNhAqVE5trsxB3omsqk282EVFRVYeR+w3BSJ8xvW1/w9TffgChJ3Gfqkg+FtFyO6MTT8Tg+1cIQiGxorDETXS8ZWTQJdVhMgCtkSxuNKDRR6rYakEVgupUGlAg4kXgMYw86aLu+f+qUKcjJzEZDfX2X/Y06+YEpNDYMNYb59Fs/0OOYr6tYEDfwvqrhh7hEZIWMsqRCFXdOX2zbB9xG/ygWjfFY3jHHHdvhfvfefQ8++vDDdj9Lz0jHaWS6G5ubfleHXehga18DCgjJBg+t5JO3ly1LKDQl5IoKCmjLI9OrmHHEiIiIptTayLX7asHuBMCKqkocMX48Ro4a1e4+LM53/Q3X45Ybb8JB48a1u88RR47H/Q8+QKbN2CmPjYWE+Fwzbezv1n8zbd3U1IRwOLw+bLSxA27NV6enp3NTxPZhU42NxPBZ2IT5qRbzNXkohgddWGchh4I0+o7LYCEVs9svmeg2AGR+m0b+0ZgxB3a4zxtvvMEfSHl5RYf7sHjg0EF7Y9ny5cjMzup0N3E26a8bOgdXc6ClXSbqlhV4vF6MooGSlp6GFatWQVW1zRxwnQbMqhUrkOT3IxqLIi01DYcddhgqq6vQ0NC4GbgYqAPNzShfuxYZGRkwuvDc9m4HwObmFqQnp2Dy5Mkd7tNqet97/z3U1dXxh7SpKA4HppxxOq669hpks6SFbQQg01AMAFXV1WgJBTGwX3+M7X0QBg4aiIKCArjdbg6aRb/+iiVLluDTzxegbG0ZLr/yLzjk0EM3SwJozey56vIr+Dxuekoq1+C9+vbBw489Cl87iQOiJKKF7sPkE0/Cx59+gpysbBuAv4+jKqC6oQ5//vOfUVRc3O4+oVAIH8//EGm+JKytrMCzzzyL666/rt19Rx80lr9qxDTFbZgL5yv4aVu6cgWySGveefffccYZZ6xfvNWefPvtt5hCpIfNQ8+cORN/+tOfNh8MioKxBx+Mx6b9A34CHEuruuHGG/H9t9/htTf+ywG/qSQnJ2PE6AMw54P3O05Hs0nITvb/RMuHOpgeVkfy2quvYsnyZchIz+A/at68eR3uu/+wYTj04ENQRkBtzz9rD3zLVq/CxKOPxk8//cQHwpbAx2S//fbjmvCII47ApEmTOtyvkUw5Z7+k7VgiRY+CIh4qmjV7VoffaQkEsLtIlwcgA0B9fT369Oy5RQB+tuBz/spMamZaOhYuXMjNcEcydeqFlvndigmWiI0y8E067ni8PWMGcrJzOnX97777LiZOnIilS5e2v0Ob8/OZgcRgY+a8QzFNG4C/h/DUdJaESc7+mWedzc1Pu/4haZG55PdlkI/ImCFz6qtrqvHcv/7V4bEPPfxwpKemEpEIdBgSYSZwZdlq7LvvvlwrtYJkm68/se8LL7yAtLS0Tn3H5XTuxPto8vliG4DbIa3scdwWtB/LhStbt279Q26dY/zg3fc6/A4D8/ijjkJdYwNntu0JC6GwLOrXXnttI43cnrz11lt45plnCPTP4eXp07nWbt2X5Sy2R4h+L2G+poPIl5FYxmCTkE6Y38qqSow54ECMHDWyw/1mzZrJAdeacs8AmEW+4MKff+Z1STpKWph64YV4+aWX6Hub58qxgHd5dRXOJs1bWlra4bkXLFiAqRddhF/oXG0llxjqIw8/jBMnn/KH30f2W5g274q5n13bBBsmB8dFl1zc4T4sLLJw4c/IIr8PrT4dbUk+H6rravHccx1nCg8jMtKzpAcaGhs3M/2hSBQ+jxd//etNHX5/yeLFfH0KA19pYTF60lZKJKI3HbORNOBJp07GO2++9cffx0Sg3DbBnZRwMIDM1DQccughHe5z3bXXoqa+DlUN9Vi5tmz9tmzNav75LbfcgpaWlna/y3LoWFyxORTcaGqOPao6OubQffZBKZGf9oSZs6nnX8D/7tOjlE/V8HraorUepbCoCB46/llnnsnNsS3dzAQzQFSTfzZ50knIzMzscD82czBixAi+7HBjdijwmYIAgWtLqfiXXHIJnn7yKYSCIbg9G4pns+TV4g5ijkxYwPnTBZ+hMCe33dV2LKySR5+xVXkfzJ2LU7Yje8cG4B9KPlQ+IX/pFZdvcb/TTjtth86Tk5+HgXsNwoeffIweRcUJ6Fqy1+C9O/zed99/DwY7NrOyNZlnA7D7meDamloMGjQQIw8YtcvPdcxxVkcA5qjzTJWEJi0gM9qR/Eb+n0WUOj4uizM6aBCtXLLMRlp3AiADQliNYfz48b/L+S66aCr69+qD2trajaa2nFuIxYUjkYTDuOXAhtftQSO5EvFYfJdHDGwA7iRh/liKL4mAcfHvcj4HAe3gQw9GE5EevnY4gUJ9C1nTrYHi1mnCjrWgYSUVCLsUffwcXTXY3K0AyOZd2bqNofsPQ1FJ8U4/fkcP6YgJE6zPtQ1gaWho6PA4vXv3Xh/i2JJWCoTDyCQ/0+HYdT1XGGGLx+Prl6l2F9m8T0gXYb/skbL5046E5eKdefoZCNHDdW1DqQmTtBCb9H/wwQc5Y25Pjj76aIweOQrff/st8nLzLD/vt986PObegwfTzRN4SlV7WSutZIZNDW5pDttmwV1M6uvq0btHT5x77rkd7vPJJ59gxqyZsNrqbFtKEmOsM2fM6BCATNiipc+++Hz91NyKFSs63HfggAEoJpLCsrTz8/I306xsIAUS8cfjieTsTDHtZIRdp/3qA804bPzhVlyvA/n0w4/4a2lxCYqKigkIW95KaEv2ePHOG2/y2jIdyXEnHM+vIRKLIonIQ+XadR2TC58Pd91zDyJk+lh6FGfQpqX1mBsRi0RR3VCP666+Bv369dup96k7FZTqVgBsXfM74aijrH+3s09NVTWmv/QSMlJSt3lFBNuLBbN/XboEb77+Rof7sam5E044AeXVlchIT8d3P/7Q4QInJiedcjLuuvNOPhOzbNVKrFq7BivL1vDg81o6xqWX/Bl333fvLhmotgneBVJZVYUDho/AUW0AuCl5/Oyzz1BRV8sLFHWO9VlH+uLLL3DKaad2uNcEIiOvv/46kQYn12R33HFHhwucmLAM5n32GYr33nsXS5ct4+fp06c3Dhp7ECYeO3HXDNROmmDDMHndGCnhXws2ANsf1eF4DIcdccQmkNlYWjOdO/0QiIj4vT7Mmz+frz7rKMZ3+OGH87xCFrsrzi/EfNKAs2fNxlF/OqrDY48/cjzfdi7KtjaUNt+l9d/GJqaN/VaH4kAzm1vPyupSi/K7jC6PEKNN9iXh3PPO7RCALFD8Epnf7NT07XLEM5gZXrwI/yNAdSR5eXm49LLLUMPyBGUJfvL1Tp08GWtWrd7u3/bee+9tkdC0J1tKYHU5XRsDTte5D5qWmtruQ2WLmW6+5ebEPayBLEm2BmwnKMSd60WLF8Ob5KObuvGqV0mS8djjj6OFRnEOsWSWprUdtos/qBdffAkjRo2Ey+2GvslxZDrPgIEDubliwd3s7BwsW7GcV2OYM2cO+g/o36lTspT8s84+G99+88023wd2DR999BEG7zOEXwfT3taAFDiYWBiqrR/o4ivyGvDpp59i4KBB3Jdue+/Y9yYedyyeffZZPPzQQ6glP5oV+7QB2HZUu1z8pjJtwxZeG+0sY2Srxhij1fXtMyFMaxYVFOIzelCjRo7kiQTtnUcRJRTTfkw0VUXvnr2wauVKIin74bbbb8c5BKitpdgzkLDs6CuvuhIF+fnIycnpwPXY3NEoLijAk9Om4ZXp02nAiBuWjgpMu4n8mooS18e+zSIGbGrwpONPgD8l2Rq8mxxWkRWU9OjBtaesyLYGbA8czFdhxKKhpnb9yG29y+xztvZWZhphO6echIR58nrcCLUEEinqQhsfynrQbNaCPdTWFHa2gLyUHl5tXR2uufpq/HPak9wnPJz81UGkcVJSUnhUn5V++3XRr5g1YyZmvv02lq9eBYcgITsjkwes2yuH3N4cLnuPlZJrIRDzigttvD52hew+sAFrJKo7MI3HShKzJQQNtXXtOzD0z9rq6o2+awNwM7ZmFVrcUhLAjt44g688E3nF+K1dS+vicVZhnp+XgJHiT+Em+eFHHsGjjzyKwsJCfiwGGgaAtevW8vzDFCI8PYtLUFlRSQRA6fA3VVfXJEC3oc0CL0VMrsKWln5ueh/YvxmwtmVmqCvNGduNarailRvJt8olYsL809ZStwUF+Zw0VVVUIB6OoLyxiWsn5qfmZmZx0860EgelGsOQIft0mK3CNOaeLDYAtwC+dQSwu+66C+ecey5v8YBEwxsGpmAgiLNPPwPvzvsAfduQIjOhYUzSnrFEzeZTzzi9fU1EvtqvPy2E3+3ZDcoM2QDcyaRc4Gn5ew/eG6lpqZt97vP5MO3pf6JHaQ8sWbWCaz6X25WIngtkWquJGIRx4fkXYPSBo9s9x5rVq3n1BFYha08Vu1vmFsSpOPC3v93Z4eclPUowf/58Xv8lrsaxqqwMq9bSVraGT+Vde801eHILDWQeuP9+HnzflalatgbsxsLW9n7y6Sd47933cMT4I9o10+PGjeMba5X166+LuG+YkprKtd6WSMTnX3yOJ56chsLsXNsHtKWDm6PISEtJxQnHH48PP/wQw4bv32EIpU/fvnzbkk/Zuv+CBZ/jyCPH85kfHgw39D32HtsmeCvhChZwZl2GxowZg7fffnuHfEomLzz3PMaMHg0tGkNOVtYeDT4bgNsgbF1IcWEhFNKGJ54wiWe4sJmUTh1D1zF79myMO+ggnHPO2byzEZvJULtopX7bBHclNpwAIatGGo1EMOOdGfjwvQ+w9z5D0H/gQAwfPpwnnLKebYwFq3GVp//X1tRgydKl+GLBAqxavgI//PADVNNACQGPTYupug2+LrkmpMtqQtJiLMDM8hBZOteP3/+ABV98wStiMbbMpuMYm2Xz1GxKLtCmfjTLrs7NzYWTfU5mfU8zu0Ji1d5m5pc1qmkvrUnXdRtxW/AL2awI03itFIRN17FVaXHSkOxmJ3k8SEtOTmSsCOuDzLph7Jn3jDCmt1++RJDRTt6nmcjQaG05YEsHzDbxylrIuttJNDA32mvPNbMxsgolbUrctQGcIhLL2ywxrFfrmtcuWNDQlu4lUqKVGPOVN5W6urpqsbGx8ftNPzhqwgQcMu5gXuZMSjRRscWWToNPkniBUbYicdMuAcwkf/TRRz+KX3/99dubVgBgeWvTX5mOZK+PtybgmbiC0GHLKXuzt003ltVdU1eHQCSMf09/GcU9SjbC2Jo1a1jS7rOy1+t9gVTh3zbN8M0iJ/urb77BxGOO4e0POKI38X1ssaXdsFUb3/jFl17CMe1Uufjll18CBQUFMwRWgHvZsmUfXHvttYe2l7HLQg5sLcE3BEZWb7nLreuzpUuxMt5s2+PB4MGDebmTIUOGbLYbW6D11FNPXTx16tRpAlvI8tZbb2X06tVr9UUXXeS176Ituyp81bqQ6vrrr5+71157HcbAyVgwLr/88jryA4/53//+Z98pW3aJtILvxhtvXBEKhY5n1cVY8SeRrWdgUfzJkyfPf+aZZ8Y+8sgjS6KJTF5bbNlZwojubbfdNv8///nP/gS+AHPt2MyRyGrKseWO7HXvvff+hHzCAaeffvqTRJGb7erutuyoVFZWskY/9VdcccXfCISHkOltYLNGrRMc61lH67LBffbZxyDVeNH06dNvIACeOWjQoKOHDx9ekpmZmcUrQNmzI7ZsiQUTPpgya2xsDHz//feLfvzxxzfffffdFw8//PAgK3uyOFFbu1X+X4ABABU7rMSNNyr1AAAAAElFTkSuQmCC';
            pdf.setFontSize(8);
            pdf.text(55, 27, 'Société AGIL De Gestion et des services S.A.G.E.S');
            pdf.text(55, 40, getStation());
            pdf.setFontSize(14);
            pdf.text(660, 33, date + " -- " + currrent_date());
            pdf.text(680, 53, 'La liste du dépense');
            pdf.addImage(logo, 'png', 20, 20, 30, 40);
            // Footer
            let str = "Page " + data.pageCount;
            if (typeof pdf.putTotalPages === 'function') {
                str = str + " of " + totalPagesExp;
            }
            pdf.setFontType("normal");
            pdf.setFontStyle('normal');
            pdf.setFontSize(11);
            pdf.text(str, 375, pdf.internal.pageSize.height - 7);
        };

        const res = pdf.autoTableHtmlToJson(document.getElementById("myTable"));
        pdf.autoTable(res.columns, res.data, {
            addPageContent: pageContent,
            tableLineColor: [189, 195, 199],
            tableLineWidth: 0.75,
            styles: {
                cellPadding: 1.5,
                overflow: 'linebreak',
                valign: 'middle',
                halign: 'center',
                lineColor: [0, 0, 0],
                lineWidth: 0.2
            },
            margin: {
                top: 70,
                left: 20,
                right: 20
            },
            headStyles: {
                fillColor: [100, 100, 100],
                fontSize: 11
            },
            bodyStyles: {
                textColor: 50
            },
            alternateRowStyles: {
                fillColor: [250, 250, 250]
            },
            startY: 75,
            drawRow: function(row, data) {
                pdf.setFontStyle('bold');
                pdf.setFontSize(10);
                if ($(row.raw[0]).hasClass("innerHeader")) {
                    pdf.setTextColor(200, 0, 0);
                    pdf.setFillColor(110, 214, 84);
                    pdf.rect(data.settings.margin.left, row.y, data.table.width, 20, 'F');
                    pdf.autoTableText("", data.settings.margin.left + data.table.width / 2, row.y + row.height / 2, {
                        halign: 'center',
                        valign: 'middle'
                    });
                }
                if (row.index % 5 === 0) {
                    const posY = row.y + row.height * 6 + data.settings.margin.bottom;
                    if (posY > pdf.internal.pageSize.height) {
                        data.addPage();
                    }
                }
            },
            drawCell: function(cell, data) {
                if ($(cell.raw).hasClass("innerHeader")) {
                    pdf.setTextColor(200, 0, 0);
                    pdf.autoTableText(cell.text + '', data.settings.margin.left + data.table.width / 2, data.row.y + data.row.height / 2, {
                        halign: 'center',
                        valign: 'middle'
                    });
                    return false;
                }
            }
        });

        if (typeof pdf.putTotalPages === 'function') {
            pdf.putTotalPages(totalPagesExp);
        }

        pdf.save(date+"_"+currrent_date()+"_Deponse_"+getStation()+".pdf");
    }

    $this.click(function(e) {
        e.preventDefault();
        $this.attr('disabled', true);
        generate(date);
    });
});