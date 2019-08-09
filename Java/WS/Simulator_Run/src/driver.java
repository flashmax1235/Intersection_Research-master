
import java.awt.geom.Point2D;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;
import java.awt.*;




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
		
		
		
		//compile python sim;
		Draw map = new Draw();
		map.setCanvasSize(400,400);
		map.setXscale(-50, 50);
		map.setYscale(-50, 50);

		// variables
	
		int vin; // also corisponds to line#
		int lane;
		double w;
		double l;
		Point2D pos = new Point2D.Double();
		ArrayList<Rectangle> cars = new ArrayList<Rectangle>();

		// Location of file to read
		File file = new File(
				"/home/maxwell/Documents/Scripts/Intersection_Research-master/carData.csv");

		//C:\Users\maxwe\Documents\Research 2019\Algorithm\Intersection_Research-master
		//"/home/maxwell/Documents/Scripts/Intersection_Research-master/carData.csv");

		
		// big data
		String[] thisLines;
		String thisLine;

		// simulation parameters
		long timeStep = 50/(100); 
		System.out.print(timeStep);
		int frames = ((12 * 100 * 2) + 4)- 1;

		try {
			Scanner scanner = new Scanner(file);

			for (int i = 2; i < frames; i = i + 2) {
				//check of pause
			
				
				
				//TimeUnit.SECONDS.sleep(timeStep);
				TimeUnit.MILLISECONDS.sleep(timeStep);
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
					if ((pos.getX() == 5 && pos.getY() == -50) || (pos.getX() == 50 && pos.getY() == 5) || (pos.getX() == -5 && pos.getY() == 50) || (pos.getX() == -50 && pos.getY() == 5)|| (pos.getX() == 0 && pos.getY() == 0)) {
						
					} else {
						map.setPenColor((vin * 15) % 256, (vin * 7) % 256, (vin * 99) % 256);
						map.filledRectangle(pos.getX(), pos.getY(), w, l);
						//map.setPenColor(Color.black);
						//map.filledCircle(pos.getX(), pos.getY(), 0.5);
						
						
					}
					
					//add all cars
					Point l1 = new Point(pos.getX() - w, pos.getY() + l);
					Point r1 = new Point(pos.getX() + w, pos.getY() - l);
					
					Rectangle tempCar = new Rectangle(l1, r1);
					cars.add(tempCar);
					

				}

				scanner = new Scanner(file);
				
				//check if any rectangle colided
				try {
				if(cars.get(0).isOverLapping(cars.get(1))) {
					System.out.println("cars colided  1 and 2");
				}else if (cars.get(1).isOverLapping(cars.get(2))) {
					System.out.println("cars colided  2 and 3");
				}else if (cars.get(0).isOverLapping(cars.get(2))) {
					System.out.println("cars colided  1 and 3");
				}else {
					System.out.println("Good  ");
				}
				}catch (Exception e) {
					// TODO: handle exception
				}
				
		
				
				//delete all cars
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