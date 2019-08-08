
import java.awt.geom.Point2D;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;
import java.awt.*;





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
					if ((pos.getX() == 5 && pos.getY() == -100) || (pos.getX() == 100 && pos.getY() == 5) || (pos.getX() == -5 && pos.getY() == 100) || (pos.getX() == -100 && pos.getY() == 5)|| (pos.getX() == 0 && pos.getY() == 0)) {

					} else {
						map.setPenColor((vin * 15) % 256, (vin * 7) % 256, (vin * 99) % 256);
						map.filledRectangle(pos.getX(), pos.getY(), w, l);
						map.setPenColor(Color.black);
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