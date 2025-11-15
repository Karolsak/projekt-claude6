# Power System Simulator - Web Application

A modern, responsive web application for simulating power system load frequency control with integral controller action. Built with pure HTML, CSS, and JavaScript - no server required!

## 🌟 Features

### Interactive Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-Time Simulation**: Instant visualization of system dynamics
- **Interactive Controls**: Drag sliders to adjust parameters dynamically
- **Beautiful UI**: Modern gradient design with smooth animations

### Advanced Capabilities
- **Dual ODE Solvers**: Switch between RK45 (4th order Runge-Kutta) and Euler methods
- **Live Charts**: Four synchronized charts using Chart.js
- **Parameter Presets**: One-click loading of Examples 7.9 and 7.10
- **Integral Control Toggle**: Compare system behavior with/without integral action

### Dynamic Visualization
Four real-time charts displaying:
1. **Frequency Deviation** - System frequency response over time
2. **Governor Response** - Governor corrective action
3. **Turbine Response** - Turbine power output
4. **Power Balance** - Comparison of load disturbance and turbine output

## 🚀 Getting Started

### Option 1: Direct Browser Opening (Recommended)
Simply open `index.html` in any modern web browser:
```bash
# On Linux/Mac
open index.html

# Or double-click the file in your file explorer
```

### Option 2: Using a Local Web Server
For best performance, serve via HTTP:

**Python 3:**
```bash
python3 -m http.server 8000
# Then open: http://localhost:8000
```

**Node.js:**
```bash
npx http-server
# Then open the displayed URL
```

**PHP:**
```bash
php -S localhost:8000
# Then open: http://localhost:8000
```

## 📱 Browser Compatibility

Tested and working on:
- ✅ Chrome/Chromium 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Opera 76+

## 🎮 How to Use

### 1. Select an Example
Click on **Example 7.9** or **Example 7.10** to load predefined parameters:

**Example 7.9:**
- High gain system (K_ps = 104)
- Large load disturbance (0.48 p.u.)
- Integral control (ki = 0.1)

**Example 7.10:**
- Standard gain system (K_ps = 100)
- Small load disturbance (0.02 p.u.)
- Compare with/without integral control

### 2. Adjust Parameters
Use the sliders to customize:
- **K_ps**: Power system gain constant (10-200)
- **t_ps**: Power system time constant (1-50 s)
- **R**: Speed regulation (0.5-10)
- **t_sg**: Governor time constant (0.1-2 s)
- **t_t**: Turbine time constant (0.1-2 s)
- **k_i**: Integral controller gain (0-1)
- **ΔP_L**: Load disturbance (0-1 p.u.)
- **Simulation Time**: Duration (10-100 s)
- **Time Step**: Solver time step (0.001-0.1 s)

### 3. Toggle Integral Control
Check/uncheck the **Integral Controller** checkbox to:
- Enable: Eliminates steady-state frequency error
- Disable: Faster response but with steady-state error

### 4. Choose ODE Solver
- **RK45**: 4th order Runge-Kutta (recommended for accuracy)
- **Euler**: Forward Euler method (faster but less accurate)

### 5. Run Simulation
Click **▶ Run Simulation** to:
- Solve the differential equations
- Update all four charts in real-time
- Display detailed results including peak deviation and steady-state error

## 📊 Understanding the Results

### Frequency Deviation Chart
Shows how system frequency deviates from nominal (50 Hz) after a load disturbance:
- **With Integral Control**: Error approaches zero
- **Without Integral Control**: Settles at non-zero error

### Results Panel
Displays key metrics:
- **Peak Frequency Deviation**: Maximum frequency drop
- **Steady-State Error**: Final frequency offset
  - Green text: Near-zero error (good!)
  - Red text: Significant error (needs integral control)

## 🔬 Technical Implementation

### Power System Model
The simulator solves four coupled differential equations:

1. **Power System Dynamics:**
   ```
   dΔf/dt = (K_ps/t_ps)·(P_t - ΔP_L) - (1/t_ps)·Δf
   ```

2. **Governor:**
   ```
   dP_g/dt = (1/t_sg)·[(-1/R)·Δf - Δp_c] - (1/t_sg)·P_g
   ```

3. **Turbine:**
   ```
   dP_t/dt = (1/t_t)·P_g - (1/t_t)·P_t
   ```

4. **Integral Controller:**
   ```
   d(∫f)/dt = Δf
   Δp_c = k_i·∫f
   ```

### State Variables
- **x[0]**: Δf - Frequency deviation (Hz)
- **x[1]**: P_g - Governor output (p.u.)
- **x[2]**: P_t - Turbine output (p.u.)
- **x[3]**: ∫Δf - Integral of frequency

### ODE Solvers

**RK45 (4th Order Runge-Kutta):**
- High accuracy
- Suitable for stiff systems
- Recommended for production use

**Euler Method:**
- Simple and fast
- Lower accuracy
- Good for educational purposes

## 🎨 Customization

### Modify Chart Colors
Edit the `initializeCharts()` function in the `<script>` section:
```javascript
chartConfig('Title', 'Y Label', '#YOUR_COLOR')
```

### Adjust Layout
Modify the CSS grid in the `.charts-grid` class:
```css
.charts-grid {
    grid-template-columns: 1fr 1fr; /* Change to 1fr for single column */
}
```

### Change Color Scheme
Update the gradient colors:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 📐 Responsive Design

The application automatically adapts to different screen sizes:

- **Desktop (>1200px)**: Side-by-side controls and charts, 2×2 chart grid
- **Tablet (768-1200px)**: Stacked layout, 2×2 chart grid
- **Mobile (<768px)**: Single column, stacked charts

## 🔍 Troubleshooting

### Charts Not Displaying
- Ensure internet connection for Chart.js CDN
- Check browser console for errors
- Try refreshing the page

### Slow Performance
- Reduce simulation time
- Increase time step (dt)
- Use Euler solver instead of RK45

### Results Seem Incorrect
- Verify parameter values are reasonable
- Check that time step isn't too large
- Try RK45 solver for better accuracy

## 📚 Educational Use

This simulator is perfect for:
- Power system engineering courses
- Control systems education
- Understanding PID/integral control
- Visualizing frequency regulation
- Comparing different solver methods

## 🆚 Comparison: Web App vs Python GUI

| Feature | Web App | Python/Tkinter |
|---------|---------|----------------|
| Installation | None - open in browser | Requires Python + packages |
| Portability | Run anywhere | Needs Python environment |
| UI Design | Modern, gradient design | Native OS widgets |
| Performance | Good for typical use | Better for heavy computation |
| Offline Use | Yes (after first load) | Yes |
| Mobile Support | Yes, fully responsive | No |

## 📝 Files Structure

```
index.html          # Complete web application (standalone)
├── HTML            # Structure and content
├── CSS             # Styling and responsive design
└── JavaScript      # Simulation logic and interactivity
    ├── PowerSystemModel class
    ├── RK45Solver class
    ├── EulerSolver class
    └── Chart.js integration
```

## 🌐 Deployment

### GitHub Pages
1. Push `index.html` to your repository
2. Go to Settings → Pages
3. Select branch and `/` (root) folder
4. Your app will be live at `https://username.github.io/repo-name/`

### Netlify
1. Drag and drop `index.html` to Netlify
2. Get instant deployment with HTTPS

### Vercel
```bash
vercel --prod
```

## 🔒 Security Notes

- No server-side code - all computation in browser
- No data transmission - everything runs locally
- No external dependencies except Chart.js CDN
- Safe to use offline (save the page with Ctrl+S)

## 🎯 Future Enhancements

Potential additions:
- [ ] Export simulation data as CSV
- [ ] Save/load custom parameter sets
- [ ] Multi-area power systems
- [ ] Renewable energy integration
- [ ] Dark mode toggle
- [ ] Comparison mode (overlay multiple simulations)

## 📖 References

Based on power system control theory:
- Example 7.9: Single-area load frequency control
- Example 7.10: Integral control effectiveness

## 🤝 Contributing

This is a standalone educational tool. Feel free to:
- Modify parameters for your use case
- Add new examples
- Enhance the UI
- Implement additional features

## 📄 License

Educational use - free to modify and distribute.

## 💡 Tips for Best Results

1. **Start with presets**: Use Example 7.9 or 7.10 as starting points
2. **Small changes**: Adjust one parameter at a time to see its effect
3. **Compare solvers**: Run same scenario with RK45 and Euler
4. **Toggle integral**: See the dramatic effect of integral control
5. **Mobile use**: Works great on tablets for presentations!

---

**Enjoy exploring power system dynamics! ⚡**

For the Python/Tkinter version, see `power_system_simulator.py`
