# image-vector-quantizer
The goal of this project is to design and produce a compressor and decompressor.
The objective is to the get the lowest Mean Squared Error (MSE) possible between the original and the reconstructed image. Since there are more than one image, the objective is to minimize the average MSE when encoding and decoding all of them.

# Quantizer
This is a vector quantizer that generate compresseds `.bin` files with rate of (at most) 1 bps.

# Usage
```bash
python3 vector_cat_encoder.py cat_image.png quantized_image.bin
python3 vector_cat_decoder.py quantized_image.bin recovered_cat_image.png
```

# Results
After encode and decode 115 grayscale images, the final average Mean Squared Error (MSE) is 74.2028. 