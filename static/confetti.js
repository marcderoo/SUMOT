/**
 * A class that manages confetti animations on the page.
 * Implements the singleton pattern to ensure only one instance exists.
 * @author Michael Beckius
 * @linkcode  https://codepen.io/bananascript/pen/EyZeWm
 */
class Confetti {
    /**
     * Creates a new Confetti instance or returns the existing one.
     */
    constructor() {
      if (Confetti._instance) {
        return Confetti._instance
      }
      Confetti._instance = this;

        /**
         * @type {HTMLDivElement} The container element for the confetti.
         */
        this.container = document.createElement('div');
        this.container.style.position = 'fixed';
        this.container.style.top      = '0';
        this.container.style.left     = '0';
        this.container.style.width    = '100%';
        this.container.style.height   = '0';
        this.container.style.overflow = 'visible';
        this.container.style.zIndex   = '9999';

        return this;
    }

    /**
     * Launches the confetti animation.
     */
    launch() {
        /**
         * Timer for adding new confetti particles.
         * @type {number | undefined}
         */
        this.timer = undefined;
        
        // Utility variables
        var random = Math.random
          , cos = Math.cos
          , sin = Math.sin
          , PI = Math.PI
          , PI2 = PI * 2
          , frame = undefined
          , confetti = [];
      
        // Particle configuration
        var spread = 1000
          , sizeMin = 10
          , sizeMax = 20 - sizeMin
          , eccentricity = 10
          , deviation = 100
          , dxThetaMin = -.1
          , dxThetaMax = -dxThetaMin - dxThetaMin
          , dyMin = .13
          , dyMax = .18
          , dThetaMin = .4
          , dThetaMax = .7 - dThetaMin;
      
        /**
         * List of color themes for the confetti.
         * @type {Array<Function>}
         */
        var colorThemes = [
          function() {
            return color(200 * random()|0, 200 * random()|0, 200 * random()|0);
          }, function() {
            var black = 200 * random()|0; return color(200, black, black);
          }, function() {
            var black = 200 * random()|0; return color(black, 200, black);
          }, function() {
            var black = 200 * random()|0; return color(black, black, 200);
          }, function() {
            return color(200, 100, 200 * random()|0);
          }, function() {
            return color(200 * random()|0, 200, 200);
          }, function() {
            var black = 256 * random()|0; return color(black, black, black);
          }, function() {
            return colorThemes[random() < .5 ? 1 : 2]();
          }, function() {
            return colorThemes[random() < .5 ? 3 : 5]();
          }, function() {
            return colorThemes[random() < .5 ? 2 : 4]();
          }
        ];

        /**
         * Creates an RGB color string.
         * @param {number} r - Red component (0-255).
         * @param {number} g - Green component (0-255).
         * @param {number} b - Blue component (0-255).
         * @returns {string} RGB color string.
         */
        function color(r, g, b) {
          return 'rgb(' + r + ',' + g + ',' + b + ')';
        }
      
        /**
         * Performs cosine interpolation.
         * @param {number} a - Start value.
         * @param {number} b - End value.
         * @param {number} t - Interpolation factor (0-1).
         * @returns {number} Interpolated value.
         */
        function interpolation(a, b, t) {
          return (1-cos(PI*t))/2 * (b-a) + a;
        }
      
        // Create a 1D Maximal Poisson Disc over [0, 1]
        var radius = 1/eccentricity, radius2 = radius+radius;

        /**
         * Creates a Poisson-disc distribution over [0, 1].
         * @returns {Array<number>} Array of values in the range [0, 1].
         */
        function createPoisson() {
          // domain is the set of points which are still available to pick from
          // D = union{ [d_i, d_i+1] | i is even }
          var domain = [radius, 1-radius], measure = 1-radius2, spline = [0, 1];
          while (measure) {
            var dart = measure * random(), i, l, interval, a, b, c, d;
      
            // Find where dart lies
            for (i = 0, l = domain.length, measure = 0; i < l; i += 2) {
              a = domain[i], b = domain[i+1], interval = b-a;
              if (dart < measure+interval) {
                spline.push(dart += a-measure);
                break;
              }
              measure += interval;
            }
            c = dart-radius, d = dart+radius;
      
            // Update the domain
            for (i = domain.length-1; i > 0; i -= 2) {
              l = i-1, a = domain[l], b = domain[i];
              // c---d          c---d  Do nothing
              //   c-----d  c-----d    Move interior
              //   c--------------d    Delete interval
              //         c--d          Split interval
              //       a------b
              if (a >= c && a < d)
                if (b > d) domain[l] = d; // Move interior (Left case)
                else domain.splice(l, 2); // Delete interval
              else if (a < c && b > c)
                if (b <= d) domain[i] = c; // Move interior (Right case)
                else domain.splice(i, 0, c, d); // Split interval
            }
      
            // Re-measure the domain
            for (i = 0, l = domain.length, measure = 0; i < l; i += 2)
              measure += domain[i+1]-domain[i];
          }
      
          return spline.sort();
        }
      
        /**
         * Represents a single confetti particle.
         * Each `Confetto` is styled, positioned, and animated independently.
         * Confetti particles have randomized properties for a varied visual effect.
         *
         * @class
         * @param {function} theme - A function that returns a color string (e.g., `'rgb(255, 0, 0)'`).
         */
        function Confetto(theme) {
          /**
           * The current animation frame number for this confetto.
           * @type {number}
           */
          this.frame = 0;

          /**
           * The outer DOM element representing the confetto.
           * This element is styled to determine its overall appearance and position.
           * @type {HTMLDivElement}
           */
          this.outer = document.createElement('div');

          /**
           * The inner DOM element nested within the outer element.
           * This element is styled for the confetto's color and transformation effects.
           * @type {HTMLDivElement}
           */
          this.inner = document.createElement('div');
          this.outer.appendChild(this.inner);
      
          var outerStyle = this.outer.style, innerStyle = this.inner.style;
          outerStyle.position = 'absolute';
          outerStyle.width  = (sizeMin + sizeMax * random()) + 'px';
          outerStyle.height = (sizeMin + sizeMax * random()) + 'px';
          innerStyle.width  = '100%';
          innerStyle.height = '100%';
          innerStyle.backgroundColor = theme();
      
          outerStyle.perspective = '50px';
          outerStyle.transform = 'rotate(' + (360 * random()) + 'deg)';

          /**
           * The CSS transform axis for the confetto's 3D rotation.
           * @type {string}
           */
          this.axis = 'rotate3D(' +
            cos(360 * random()) + ',' +
            cos(360 * random()) + ',0,';

          /**
           * The initial angle of rotation for the confetto.
           * @type {number}
           */
          this.theta = 360 * random();

          /**
           * The rate of change of rotation angle per animation frame.
           * @type {number}
           */
          this.dTheta = dThetaMin + dThetaMax * random();
          innerStyle.transform = this.axis + this.theta + 'deg)';
          
          /**
           * The horizontal position of the confetto.
           * @type {number}
           */
          this.x = window.innerWidth * random();

          /**
           * The vertical position of the confetto.
           * @type {number}
           */
          this.y = -deviation;

          /**
           * The horizontal velocity of the confetto.
           * @type {number}
           */
          this.dx = sin(dxThetaMin + dxThetaMax * random());
          
          /**
           * The vertical velocity of the confetto.
           * @type {number}
           */
          this.dy = dyMin + dyMax * random();
          outerStyle.left = this.x + 'px';
          outerStyle.top  = this.y + 'px';
      
          /**
           * A periodic spline defining the horizontal movement of the confetto.
           * @type {number[]}
           */
          this.splineX = createPoisson();

          /**
           * A periodic spline defining the vertical deviation of the confetto.
           * @type {number[]}
           */
          this.splineY = [];
          for (var i = 1, l = this.splineX.length-1; i < l; ++i)
            this.splineY[i] = deviation * random();
          this.splineY[0] = this.splineY[l] = deviation * random();
      
          /**
           * Updates the position and appearance of the confetto based on elapsed time.
           * This method is called on each animation frame.
           *
           * @param {number} height - The height of the viewport, used to determine when the confetto goes out of view.
           * @param {number} delta - The time elapsed since the last frame in milliseconds.
           * @returns {boolean} - Returns `true` if the confetto is out of bounds and should be removed.
           */
          this.update = function(height, delta) {
            this.frame += delta;
            this.x += this.dx * delta;
            this.y += this.dy * delta;
            this.theta += this.dTheta * delta;
      
            // Compute spline and convert to polar
            var phi = this.frame % 7777 / 7777, i = 0, j = 1;
            while (phi >= this.splineX[j]) i = j++;
            var rho = interpolation(
              this.splineY[i],
              this.splineY[j],
              (phi-this.splineX[i]) / (this.splineX[j]-this.splineX[i])
            );
            phi *= PI2;
      
            outerStyle.left = this.x + rho * cos(phi) + 'px';
            outerStyle.top  = this.y + rho * sin(phi) + 'px';
            innerStyle.transform = this.axis + this.theta + 'deg)';
            return this.y > height+deviation;
          };
        }
      
        /**
         * Initiates the confetti animation.
         */
        function poof() {
          if (!frame) {
            // Append the this.container
            document.body.appendChild(new Confetti().container);
      
            // Add confetti
            var theme = colorThemes[0];
            (function addConfetto() {
              var confetto = new Confetto(theme);
              confetti.push(confetto);
              new Confetti().container.appendChild(confetto.outer);
              new Confetti().timer = setTimeout(addConfetto, spread * random());
            })(0);
      
            // Start the loop
            var prev = undefined;
            requestAnimationFrame(function loop(timestamp) {
              var delta = prev ? timestamp - prev : 0;
              prev = timestamp;
              var height = window.innerHeight;
      
              for (var i = confetti.length-1; i >= 0; --i) {
                if (confetti[i].update(height, delta)) {
                    new Confetti().container.removeChild(confetti[i].outer);
                  confetti.splice(i, 1);
                }
              }
      
              if (new Confetti().timer || confetti.length)
                return frame = requestAnimationFrame(loop);
      
              // Cleanup
              document.body.removeChild(new Confetti().container);
              frame = undefined;
            });
          }
        }
      
        poof();
      };

    /**
     * Stops the confetti animation.
     */
      stop() {
        if (this.timer) {
            clearTimeout(this.timer);
            this.timer = null;
        }
        if (this.frame) {
            cancelAnimationFrame(this.frame);
            this.frame = null;
        }
      }
  }