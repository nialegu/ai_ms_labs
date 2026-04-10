package com.example.dog_classifier

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import org.tensorflow.lite.Interpreter
import java.io.FileInputStream
import java.nio.MappedByteBuffer
import java.nio.channels.FileChannel

class MainActivity : AppCompatActivity() {

    private lateinit var interpreter: Interpreter
    private lateinit var labels: List<String>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        interpreter = Interpreter(loadModelFile())
        labels = loadLabels()

        val button = findViewById<Button>(R.id.btn_classify)
        val imageView = findViewById<ImageView>(R.id.image)

        button.setOnClickListener {
            val bitmap = BitmapFactory.decodeResource(resources, R.drawable.test_dog)
            val result = classify(bitmap)
            Toast.makeText(this, result, Toast.LENGTH_LONG).show()
        }
    }

    private fun loadModelFile(): MappedByteBuffer {
        val fileDescriptor = assets.openFd("dogs_model_quant.tflite")
        val inputStream = FileInputStream(fileDescriptor.fileDescriptor)
        val fileChannel = inputStream.channel
        return fileChannel.map(
            FileChannel.MapMode.READ_ONLY,
            fileDescriptor.startOffset,
            fileDescriptor.declaredLength
        )
    }

    private fun loadLabels(): List<String> {
        return assets.open("dog_labels.txt")
            .bufferedReader()
            .readLines()
    }

    private fun classify(bitmap: Bitmap): String {
        val input = preprocess(bitmap)
        val output = Array(1) { FloatArray(labels.size) }

        interpreter.run(input, output)

        val results = output[0]
            .mapIndexed { i, v -> i to v }
            .sortedByDescending { it.second }
            .take(5)

        return results.joinToString("\n") {
            "${labels[it.first]}: ${(it.second * 100).toInt()}%"
        }
    }

    private fun preprocess(bitmap: Bitmap): Array<Array<Array<FloatArray>>> {
        val resized = Bitmap.createScaledBitmap(bitmap, 224, 224, true)

        val input = Array(1) { Array(224) { Array(224) { FloatArray(3) } } }

        for (y in 0 until 224) {
            for (x in 0 until 224) {
                val pixel = resized.getPixel(x, y)

                input[0][y][x][0] = (Color.red(pixel) - 127.5f) / 127.5f
                input[0][y][x][1] = (Color.green(pixel) - 127.5f) / 127.5f
                input[0][y][x][2] = (Color.blue(pixel) - 127.5f) / 127.5f
            }
        }

        return input
    }
}