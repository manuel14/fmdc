function loadBanners(banners) {
	let images = []

	function clearImages() {
		let imagesToDelete = document.getElementsByClassName('banner-img')
		for (let index = 0; index < imagesToDelete.length; index++) {
			imagesToDelete[index].style.display = 'none';
		}
	}

    function crearImagenes(url) {
		var newImg = new Image();
        var objectURL = URL.createObjectURL(url);
		newImg.src = objectURL;
        newImg.width = 240;
        newImg.heigth = 120;
		newImg.className = 'banner-img';
        newImg.style.display = "none";
        newImg.style.margin = '0px auto 0px auto';
        banner = document.getElementById('banner');
        banner.appendChild(newImg);
		return newImg;
	}
	
    clearImages()
    $.each(banners, function(_, val) {
        images.push(crearImagenes(val));
    });

    function hideImage(image, index) {
        image.style.display = "none";
        if (index) {
            images[index].style.display = 'block';
        }
    }

    images[0].style.display = 'block';
    setTimeout(hideImage, 5000, images[0], 1);
    setTimeout(hideImage, 15000, images[1], 2);
    setTimeout(hideImage, 25000, images[2], 3)
    setTimeout(hideImage, 35000, images[3])

}


