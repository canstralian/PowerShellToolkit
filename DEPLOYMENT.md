# Deploying ReconNINJ@ to Production

This guide outlines the steps to deploy ReconNINJ@ to a production environment using Replit.

## Prerequisites

- A Replit account
- Basic knowledge of Python and PowerShell
- Familiarity with web application deployment

## Deployment Steps

1. **Fork the ReconNINJ@ Repository**
   - Go to the ReconNINJ@ repository on Replit
   - Click on the "Fork" button to create your own copy of the project

2. **Configure Environment Variables**
   - In your forked Replit project, go to the "Secrets" tab
   - Add any necessary environment variables, such as:
     - `OPENWEATHERMAP_API_KEY` (if used for weather functionality)
     - `LOG_LEVEL` (e.g., INFO, DEBUG, ERROR)
     - `SCRIPT_URL` (URL for self-regeneration feature)
     - `EXFILTRATION_URL` (URL for data exfiltration)

3. **Install Dependencies**
   - Open the Shell in Replit
   - Run the following command to install required Python packages:
     ```
     pip install -r requirements.txt
     ```

4. **Set Up the Run Configuration**
   - In the Replit interface, click on the "Run" button at the top
   - Set the run command to:
     ```
     python recon_ninja.py
     ```

5. **Configure Replit for PowerShell (if needed)**
   - If PowerShell functionality is required, you may need to use a custom Replit configuration
   - Create or modify the `.replit` file in the project root with the following content:
     ```
     language = "powershell"
     run = "pwsh ReconNINJA.ps1"
     ```

6. **Start the Application**
   - Click the "Run" button in Replit to start the ReconNINJ@ application

7. **Access the Web Interface**
   - Once the application is running, Replit will provide a URL to access the web interface
   - Click on the provided URL to open the ReconNINJ@ GUI in a new tab

8. **Set Up Continuous Deployment (Optional)**
   - Enable GitHub integration in your Replit project
   - Connect your Replit project to a GitHub repository
   - Configure automatic deployments when changes are pushed to the main branch

## Monitoring and Logging

- Logs are stored in `ReconNINJA.log` and `gui_log.txt`
- Monitor these logs for any errors or issues
- Consider implementing additional monitoring tools as needed

## Scaling Considerations

- Replit has limitations for long-running processes and resource usage
- For high-traffic applications, consider migrating to a more robust hosting solution

## Security Considerations

- Regularly update dependencies to patch any vulnerabilities
- Implement proper authentication and authorization for admin functions
- Use HTTPS for all communications (Replit provides this by default)
- Ensure that the `SCRIPT_URL` and `EXFILTRATION_URL` are secure and use HTTPS
- Implement additional security measures for the self-regeneration and data exfiltration features

## Backup and Disaster Recovery

- Regularly backup your Replit project
- Consider exporting critical data and configurations periodically

## New Features Deployment Considerations

### Random Execution Delays
- No additional setup required, but be aware that the application may have variable response times

### Uptime Checks
- Ensure that the hosting environment allows for accurate system uptime reporting

### Self-Regeneration
- Set up a secure location to host the latest version of the script
- Ensure that the `SCRIPT_URL` environment variable is correctly set

### Enhanced Data Exfiltration
- Set up a secure endpoint to receive exfiltrated data
- Ensure that the `EXFILTRATION_URL` environment variable is correctly set

## Troubleshooting

- If the application fails to start, check the Replit console for error messages
- Verify that all required environment variables are set correctly
- Ensure all dependencies are installed properly
- Check the logs for any issues related to the new features (random delays, uptime checks, self-regeneration, data exfiltration)

For any additional support or questions, please refer to the project's README.md or open an issue in the GitHub repository.
