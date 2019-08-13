
import java.awt.geom.Point2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;
import java.awt.*;
import javax.swing.*;

class Point {
	double x;
	double y;

	public Point(double d, double e) {
		super();
		this.x = d;
		this.y = e;
	}
}

class Rectangle {

	private final Point topLeft;
	private final Point bottomRight;

	public Rectangle(Point topLeft, Point bottomRight) {
		this.topLeft = topLeft;
		this.bottomRight = bottomRight;
	}

	/**
	 * Java method to check if two rectangle are intersecting to each other.
	 * 
	 * @param other
	 * @return true if two rectangle overlap with each other
	 */
	public boolean isOverLapping(Rectangle other) {

		if (this.topLeft.x > other.bottomRight.x // R1 is right to R2
				|| this.bottomRight.x < other.topLeft.x // R1 is left to R2
				|| this.topLeft.y < other.bottomRight.y // R1 is above R2
				|| this.bottomRight.y > other.topLeft.y) { // R1 is below R1
			return false;
		}
		return true;
	}

	public String toString() {
		return (this.topLeft + "    " + this.bottomRight);
	}

}

public class driver {

	public static void main(String[] args) throws InterruptedException {

		// compile python sim;
		Draw map = new Draw();
		map.setCanvasSize(400,400);
		map.setXscale(-75, 75);
		map.setYscale(-75, 75);

		// variables

		int vin; // also corisponds to line#
		int lane;
		double w;
		double l;
		BufferedImage img;
		Graphics2D g2;
		Point2D pos = new Point2D.Double();
		ArrayList<Rectangle> cars = new ArrayList<Rectangle>();

		// Location of file to read
		File file = new File("/home/maxwell/Documents/Scripts/Intersection_Research-master/carData.csv");

		// C:\Users\maxwe\Documents\Research 2019\Algorithm\Intersection_Research-master
		// "/home/maxwell/Documents/Scripts/Intersection_Research-master/carData.csv");

		// big data
		String[] thisLines;
		String thisLine;

		// simulation parameters
		long timeStep = 50 / (100);
		System.out.print(timeStep);
		int frames = ((12 * 100 * 2) + 4) - 1;

		img = new BufferedImage(150, 150, BufferedImage.TYPE_INT_RGB);
		g2 = (Graphics2D) img.getGraphics();
		JFrame theWindow = new JFrame("Simulation");

		try {
			Scanner scanner = new Scanner(file);

			for (int i = 2; i < frames; i = i + 2) {

				// TimeUnit.SECONDS.sleep(timeStep);
				TimeUnit.MILLISECONDS.sleep(timeStep * 2);
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
					l = Double.parseDouble(thisLines[2]);
					w = Double.parseDouble(thisLines[3]);

					if (i > 1) {
						// System.out.print(Double.parseDouble(thisLines[i]) + " " +
						// Double.parseDouble(thisLines[i+1]) );
						pos.setLocation(Double.parseDouble(thisLines[i]), Double.parseDouble(thisLines[i + 1]));
					}
					if ((pos.getX() == 5 && pos.getY() == -75) || (pos.getX() == 75 && pos.getY() == 5)
							|| (pos.getX() == -5 && pos.getY() == 75) || (pos.getX() == -75 && pos.getY() == 5)
							|| (pos.getX() == 0 && pos.getY() == 0)) {

					} else {
						//g2.setColor(new Color((vin * 15) % 256, (vin * 7) % 256, (vin * 99) % 256));
						//g2.fillRect((int) pos.getX(), (int) pos.getY(), (int) w, (int) l);
						//g2.drawImage(img, 0, 0, null);

						map.setPenColor((vin * 15) % 256, (vin * 7) % 256, (vin * 99) % 256);
						map.filledRectangle(pos.getX(), pos.getY(), w, l);

						// add acar
						Point l1 = new Point(pos.getX() - w, pos.getY() + l);
						Point r1 = new Point(pos.getX() + w, pos.getY() - l);

						Rectangle tempCar = new Rectangle(l1, r1);
						cars.add(tempCar);

					}

				}
				g2.clearRect(0, 0, 75, 75);

				scanner = new Scanner(file);

				// check if any rectangle colided
				for (int j = 0; j < cars.size(); j++) {
					for (int j2 = 0; j2 < cars.size(); j2++) {
						if ((cars.get(j).isOverLapping(cars.get(j2))) && (j2 != j)) {
							System.out.println(j + " -- " + j2);
						}
					}
				}

				// delete all cars
				cars.clear();

			}
			scanner.close();
		} catch (

		FileNotFoundException e) {
			e.printStackTrace();
		}

		System.out.println("done");

	}
}