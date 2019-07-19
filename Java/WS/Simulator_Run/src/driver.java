import java.awt.List;
import java.awt.geom.Point2D;
import java.util.ArrayList;

import javax.swing.plaf.synth.SynthToggleButtonUI;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

public class driver {

	public static void main(String[] args) throws InterruptedException {
		
		
		
		//compile python sim
		Complex check = new Complex(0, 0);
		Draw map = new Draw();
		map.setCanvasSize(800, 800);
		map.setXscale(-100, 100);
		map.setYscale(-100, 100);

		// variables
		String[] data;
		int vin; // also corisponds to line#
		int lane;
		double delta = 0;
		int counter = 0; // 0 and 1 read in land and vin, after that are points
		Point2D pos = new Point2D.Double();

		// Location of file to read
		File file = new File(
				"/home/maxwell/Documents/Scripts/Intersection_Research-master/carData.csv");

		//C:\Users\maxwe\Documents\Research 2019\Algorithm\Intersection_Research-master
		//"/home/maxwell/Documents/Scripts/Intersection_Research-master/carData.csv");

		
		// big data
		String[] thisLines;
		String thisLine;

		// simulation parameters
		long timeStep = 250000/2; // microseconds  1/(20 * frames)
		int frames = 200 * 2 + 2;

		try {
			Scanner scanner = new Scanner(file);

			for (int i = 0; i < frames; i = i + 2) {
				TimeUnit.MICROSECONDS.sleep(timeStep);
				map.clear();
				
				map.square(-5, -5, 2.5);
				map.square(5, -5, 2.5);
				map.square(5, 5 , 2.5);
				map.square(-5, 5, 2.5);
				
				
				while (scanner.hasNextLine()) { // iterte through row
					thisLine = scanner.nextLine();
					// System.out.println(thisLine);
					// get vin* and lane
					thisLines = thisLine.split(",");
					vin = (int) Double.parseDouble(thisLines[0]);
					lane = (int) Double.parseDouble(thisLines[1]);

					if (i > 1) {
						// System.out.print(Double.parseDouble(thisLines[i]) + " " +
						// Double.parseDouble(thisLines[i+1]) );
						pos.setLocation(Double.parseDouble(thisLines[i]), Double.parseDouble(thisLines[i + 1]));
					}
					if ((pos.getX() == 5 && pos.getY() == -100) || (pos.getX() == 100 && pos.getY() == 5) || (pos.getX() == -5 && pos.getY() == 100) || (pos.getX() == -100 && pos.getY() == 5)) {

					} else {
						map.setPenColor((vin * 15) % 256, (vin * 7) % 256, (vin * 99) % 256);
						map.filledCircle(pos.getX(), pos.getY(), 0.5);
					}

				}

				scanner = new Scanner(file);
			}

			scanner.close();
		} catch (

		FileNotFoundException e) {
			e.printStackTrace();
		}

		System.out.println("done");

	}
}
