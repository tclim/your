using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

using System.Net;
using System.Net.Sockets;

namespace URScriptSender
{
    public partial class FormYourUR : Form
    {

        // Variables
        protected string robotIP = null;
        protected int robotPort = 0;

        public FormYourUR()
        {
            InitializeComponent();
        }

        #region Edit Menu Code

        private void undoToolStripMenuItem_Click(object sender, EventArgs e)
        {
            txtPad.Undo();
        }

        private void cutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            txtPad.Cut();
        }

        private void copyToolStripMenuItem_Click(object sender, EventArgs e)
        {
            txtPad.Copy();
        }

        private void pasteToolStripMenuItem_Click(object sender, EventArgs e)
        {
            txtPad.Paste();
        }

        private void selectAllToolStripMenuItem_Click(object sender, EventArgs e)
        {
            txtPad.SelectAll();
        }

    #endregion

        #region File Menu Code

        private void newToolStripMenuItem_Click(object sender, EventArgs e)
        {
            txtPad.Clear();
        }

        private void openToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Create OFD
            OpenFileDialog sfdOpenFile = new OpenFileDialog();

            //Set SFD Properties
            sfdOpenFile.Title = "Select a URScript text file to open";
            sfdOpenFile.FileName = "";
            sfdOpenFile.Filter = "Text File (*.txt)|*.txt";

            //Execute
            if (sfdOpenFile.ShowDialog() == DialogResult.OK)
            {
                txtPad.LoadFile(sfdOpenFile.FileName, RichTextBoxStreamType.PlainText);
            }
        }

        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            //Create SFD
            SaveFileDialog sfdSaveFile = new SaveFileDialog();
            
            //Set SFD Properties
            sfdSaveFile.Title = "Save Your URScript";
            sfdSaveFile.FileName = "";
            sfdSaveFile.Filter = "Text File (*.txt)|*.txt";

            //Execute
            if (sfdSaveFile.ShowDialog() == DialogResult.OK)
            {
                txtPad.SaveFile(sfdSaveFile.FileName, RichTextBoxStreamType.PlainText);
            }
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Close();
        }

        #endregion

        #region Control Code
        private void textBoxIP_TextChanged(object sender, EventArgs e)
        {
            robotIP = textBoxIP.Text;
        }

        private void textBoxPort_TextChanged(object sender, EventArgs e)
        {
            robotPort = Convert.ToInt32(textBoxPort.Text);
        }

        #endregion 

        private void button1Send_Click(object sender, EventArgs e)
        {
            //Check if IP and Port are valid
            if (robotIP == null || robotPort == 0)
            {
                txtCommandLog.Text = "Make sure IP and Port are specified";
                return;
            }
            
            //Create Socket
            IPAddress _ip = IPAddress.Parse(robotIP);
            IPEndPoint ipe = new IPEndPoint(_ip, robotPort);
            Socket mySocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            //Attempt to send to 
            try
            {
                mySocket.Connect(ipe);
                txtCommandLog.Text = "Attempting to Connect to Robot...";
               
                //Simple read for now
                ASCIIEncoding encoding = new ASCIIEncoding();
                
                if (txtPad.Text != null)
                {
                    byte[] msgBytes = encoding.GetBytes(txtPad.Text);
                    txtCommandLog.Text += "\nSending URScript..";

                    mySocket.Send(msgBytes);
                    mySocket.Close();
                    txtCommandLog.Text += "\nFinished Sending...";
                }
            }
            catch (ArgumentNullException ae)
            {
                txtCommandLog.Text += ("\nArgumentNullException : {0} " + ae.ToString());
            }
            catch (SocketException se)
            {
                txtCommandLog.Text += ("\nSocketException : {0} " + se.ToString());
            }
            catch (Exception ex)
            {
                txtCommandLog.Text += ("\nUnexpected exception : {0} " + ex.ToString());
            }     
        }

        private void txtCommandLog_TextChanged(object sender, EventArgs e)
        {

        }


    }
}
