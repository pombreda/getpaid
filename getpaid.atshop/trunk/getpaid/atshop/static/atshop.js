/**
 * Shopping related Javascripts functions
 */


// Declare namespace
atshop = {};


/**
 * Allow fancy zoom rendering of the images on click
 * on the product page.
 */
atshop.setupProductImagePreviews = function() {
	jq('.product-images a.image-opener').fancyZoom({closeOnClick: true})
}
