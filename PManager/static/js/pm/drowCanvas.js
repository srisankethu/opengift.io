/*
	// JavaScript 
	$("#canvasPaint").drawCanvas({
		colors: ['rgb(212,21,29)', 'rgb(131,190,61)']
	});

	// HTML
     <div id="canvasPaint">
         <div class="canvasTools">
             <div class="brushColor"></div>
             <div class="brushDepth"></div>
         </div>
         <div class="CanvasContainer"></div>
         <div class="canvasBottons">
             <button class="canvasSave">Сохранить</button>
             <button class="canvasClear">Очистить</button>
         </div>
         <div id="savedCopyContainer"></div>
     </div>
*/
(function($){
	$.fn.drawCanvas = function(options) {
		options = $.extend({
            rezImg: '',
			width: '700px',
			height: '400px',
			colors: ['rgb(212,21,29)', 'rgb(131,190,61)', 'rgb(0,86,166)'],
			sizes: [1, 4, 6],
			onImages: { // параметры изображение
				img: '', // jQuery элемент img
				x: 0, // x верхная точка
				y: 0, // y верхная точка
				w: 0, // width изображение
				h: 0 // height изображение
			}
		}, options);

		var context, canvas, previousThicknessElement, brashInColor,
			canImg = options.onImages,
			isDrawing = false,
			windowWidth = $(window).width(),
			windowHeight = $(window).height(),
			canvasBlock = $(this).find(".CanvasContainer"), // Блок для canvas
			colorBlock = $(this).find(".brushColor"), // Блок для цветов
			depthBlock = $(this).find(".brushDepth"), // Блок для линии
			saveButton = $(this).find(".canvasSave"), // Кпонка сохранить
			clearButton = $(this).find(".canvasClear"), // Кнопка очистить
			textButton = $(this).find(".canvasText"), // Кнопка текст
			saveImgBlock = $(this).find("#savedCopyContainer");

		if(options.colors.length) {//Инициализация цвет киста
			for(var i=0; i<options.colors.length; i++) {
				if(i == 0)
					colorBlock.append('<div class="color active" style="background: '+options.colors[i]+';" rgbColor="'+options.colors[i]+'"></div>');
				else
					colorBlock.append('<div class="color" style="background: '+options.colors[i]+';" rgbColor="'+options.colors[i]+'"></div>');
			}
		}

		if(options.sizes.length){//Инициализация размер киста
			for(var i=0; i<options.sizes.length; i++){
				if(i == 0)
					depthBlock.append('<div class="size active" id="size_'+options.sizes[i]+'" relSize="'+options.sizes[i]+'"></div>');
				else
					depthBlock.append('<div class="size" id="size_'+options.sizes[i]+'" relSize="'+options.sizes[i]+'"></div>');
			}
		}

		// Инициализация элемента canvas
		canvasBlock.html('<canvas id="drawingCanvas" width="'+options.width+'" height="'+options.height+'"></canvas>');
		canvas = $(this).find("#drawingCanvas");
		context = canvas[0].getContext("2d");

		if(options.onImages != ''){
			var image = new Image();
			image.src = canImg.img.attr("src");
			context.drawImage(image, canImg.x, canImg.y, canImg.w, canImg.h, 0, 0, canImg.w, canImg.h);
            saveCanvas();
		}

		//Обработка событие на canvas элементе
		canvas.mousedown(function(e){
			if (depthBlock.find('.size').hasClass('active')) {
				startDrawing(e);
			} else {
				writeText();
			};
		});
		canvas.mousemove(function(e){ draw(e) });
		canvas.bind("mouseup mouseover", function(){ stopDrawing() });

		// Обработка кнопки "Очистить"
		clearButton.on("click", function(){ clearCanvas() });
		// Обработка кнопки "Сохранить"
		//saveButton.on("click", function(){ saveCanvas() });

		// Обработка кнопки "Текст"
		textButton.on("click", function(){
			depthBlock.find('.size.active').removeClass('active');
			$(this).addClass('active');
			canvas.removeClass('drawing').addClass('writeText');
		});

		// Меняеть цвет киста
		brashInColor = options.colors[0];
		context.strokeStyle = brashInColor;

		colorBlock.find(".color").on("click", function(){
			brashInColor = $(this).attr("rgbcolor"); //Получить цвет
			context.strokeStyle = brashInColor; // Установить цвет
			$('.CanvasContainer').css('color', brashInColor); // Цвет текста
			$(this).siblings().removeClass("active").end().addClass("active");
		});

		// Меняет диаметр киста
		context.lineWidth = options.sizes[0]

		depthBlock.find(".size").on("click", function(){
			var getBrushLineWidth = $(this).attr("relsize");
			context.lineWidth = getBrushLineWidth;
			textButton.removeClass('active');
			$(this).siblings().removeClass("active").end().addClass("active");
			$(canvas).removeClass('writeText');
		});

		// Функции
		function writeText() {
			canvas.click(function(e){
				if ($('.writeTextContainer').length == 0 && textButton.hasClass('active')) {
				    var offset = $(this).offset();
				    var scrollTop = $('.CanvasContainer').scrollTop();
				    var scrollLeft = $('.CanvasContainer').scrollLeft();
				    var x = e.pageX - offset.left + 16 - scrollLeft;
				    var y = e.pageY - offset.top + 62 - scrollTop;
				    $('.CanvasContainer').prepend('<div class="writeTextContainer"><textera class="writeText" contenteditable="true"></textera><div class="buttons clearfix"><a href="#" class="remove btn btn-danger btn-mini"><i class="fa fa-times icon-remove icon-white"></i></a><a href="#" class="apply btn btn-success btn-mini"><i class="fa fa-check icon-remove icon-white"></i></a></div></div>');
				    $('.writeTextContainer').css('left', x).css('top', y);
					$('.writeTextContainer .writeText').focus();
				
					$('.writeTextContainer .apply').on("click", function(){
						var text = $('.writeTextContainer .writeText').text();
						context.fillStyle = brashInColor;
					    context.font = "25px Arial";
					    context.fillText(text, x - 16.5 + scrollLeft, y - 54 + scrollTop);
					    $('.writeTextContainer').remove();
					    return false;
					});

					$('.writeTextContainer .remove').on("click", function(){
						$('.writeTextContainer').remove();
						return false;
					});
				};
			});
		}

		function startDrawing(e) {
			isDrawing = true;
			context.beginPath();
			context.moveTo(e.pageX - canvas.offset().left, e.pageY - canvas.offset().top);
		}

		function stopDrawing() {
		    isDrawing = false;
            saveCanvas();
		}

		function draw(e) {
			if (isDrawing == true)
			{
				var x = e.pageX - canvas.offset().left;
				var y = e.pageY - canvas.offset().top;

				context.lineTo(x, y);
				context.stroke();
			}
		}

		function clearCanvas() {
			context.clearRect(0, 0, canvasBlock.width(), canvasBlock.height());
			context.drawImage(image, canImg.x, canImg.y, canImg.w, canImg.h, 0, 0, canImg.w, canImg.h);
		}

		function saveCanvas() {
			can = canvas[0];
			var data = can.toDataURL('image/png'); // получаем data:image/png;base64
            if(options.rezImg != ''){
                options.rezImg.val(data);
            }
		}
		
	};
})(jQuery);