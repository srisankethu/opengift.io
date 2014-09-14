/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 22.08.14
 * Time: 18:16
 */
var FULLSCREEN = {
    fullScreenElement: function (element) {
        if (element.requestFullscreen) {
            element.requestFullscreen();
        } else if (element.webkitrequestFullscreen) {
            element.webkitRequestFullscreen();
        } else if (element.mozRequestFullScreen) {
            element.mozRequestFullScreen();
        }
    },
    exitFullscreen: function () {
        if (document.requestFullscreen) {
            document.requestFullscreen();
        } else if (document.webkitRequestFullscreen) {
            document.webkitRequestFullscreen();
        } else if (document.mozRequestFullscreen) {
            document.mozRequestFullScreen();
        }
    }
}