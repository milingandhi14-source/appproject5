
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class StudentAttendanceSystem extends JFrame {

    JTextField nameField;
    JTable table, historyTable;

    DefaultTableModel model, historyModel;

    Color background = new Color(20, 27, 45);
    Color blue = new Color(55, 125, 210);

    public StudentAttendanceSystem() {

        setTitle("Student Attendance System");
        setSize(950, 600);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        JTabbedPane tabs = new JTabbedPane();

        tabs.addTab("Attendance", attendancePanel());
        tabs.addTab("Attendance History", historyPanel());

        add(tabs);
    }

    // ---------------- ATTENDANCE PANEL ----------------

    JPanel attendancePanel() {

        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBackground(background);

        JLabel heading = new JLabel("STUDENT ATTENDANCE SYSTEM");
        heading.setFont(new Font("Arial", Font.BOLD, 25));
        heading.setForeground(Color.WHITE);
        heading.setHorizontalAlignment(JLabel.CENTER);

        panel.add(heading, BorderLayout.NORTH);

        // Input section
        JPanel inputPanel = new JPanel();
        inputPanel.setBackground(background);

        nameField = new JTextField(18);
        JButton addButton = createButton("Add Student");

        JLabel nameLabel = new JLabel("Student Name:");
        nameLabel.setForeground(Color.WHITE);

        inputPanel.add(nameLabel);
        inputPanel.add(nameField);
        inputPanel.add(addButton);

        // Student table
        String[] columns = {
            "Student Name", "Today's Status",
            "Present", "Total Classes", "Percentage"
        };

        model = new DefaultTableModel(columns, 0);
        table = new JTable(model);
        table.setRowHeight(30);

        JScrollPane scrollPane = new JScrollPane(table);

        // Buttons
        JPanel buttonPanel = new JPanel();
        buttonPanel.setBackground(background);

        JButton presentButton = createButton("Mark Present");
        JButton absentButton = createButton("Mark Absent");
        JButton saveButton = createButton("Save Attendance");

        buttonPanel.add(presentButton);
        buttonPanel.add(absentButton);
        buttonPanel.add(saveButton);

        JPanel center = new JPanel(new BorderLayout(10, 10));
        center.setBackground(background);

        center.add(inputPanel, BorderLayout.NORTH);
        center.add(scrollPane, BorderLayout.CENTER);
        center.add(buttonPanel, BorderLayout.SOUTH);

        panel.add(center, BorderLayout.CENTER);

        // Button actions
        addButton.addActionListener(e -> addStudent());

        presentButton.addActionListener(e -> markStatus("Present"));

        absentButton.addActionListener(e -> markStatus("Absent"));

        saveButton.addActionListener(e -> saveAttendance());

        return panel;
    }

    // ---------------- HISTORY PANEL ----------------

    JPanel historyPanel() {

        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBackground(background);

        JLabel heading = new JLabel("ATTENDANCE HISTORY");
        heading.setFont(new Font("Arial", Font.BOLD, 24));
        heading.setForeground(Color.WHITE);
        heading.setHorizontalAlignment(JLabel.CENTER);

        panel.add(heading, BorderLayout.NORTH);

        String[] columns = {
            "Date", "Student Name", "Attendance Status"
        };

        historyModel = new DefaultTableModel(columns, 0);
        historyTable = new JTable(historyModel);
        historyTable.setRowHeight(30);

        JScrollPane scrollPane = new JScrollPane(historyTable);

        panel.add(scrollPane, BorderLayout.CENTER);

        JButton clearButton = createButton("Clear History");

        clearButton.addActionListener(e -> {
            int choice = JOptionPane.showConfirmDialog(
                this,
                "Delete all attendance history?",
                "Confirm",
                JOptionPane.YES_NO_OPTION
            );

            if (choice == JOptionPane.YES_OPTION) {
                historyModel.setRowCount(0);
            }
        });

        panel.add(clearButton, BorderLayout.SOUTH);

        return panel;
    }

    // ---------------- ADD STUDENT ----------------

    void addStudent() {

        String name = nameField.getText().trim();

        if (name.isEmpty()) {
            JOptionPane.showMessageDialog(this,
                "Please enter student name!");
            return;
        }

        // Prevent duplicate student names
        for (int i = 0; i < model.getRowCount(); i++) {
            if (model.getValueAt(i, 0).toString()
                    .equalsIgnoreCase(name)) {
                JOptionPane.showMessageDialog(this,
                    "Student already exists!");
                return;
            }
        }

        model.addRow(new Object[]{
            name, "Pending", 0, 0, "0%"
        });

        nameField.setText("");
    }

    // ---------------- MARK ATTENDANCE ----------------

    void markStatus(String status) {

        int row = table.getSelectedRow();

        if (row == -1) {
            JOptionPane.showMessageDialog(this,
                "Please select a student!");
            return;
        }

        model.setValueAt(status, row, 1);
    }

    // ---------------- SAVE ATTENDANCE ----------------

    void saveAttendance() {

        if (model.getRowCount() == 0) {
            JOptionPane.showMessageDialog(this,
                "Please add students first!");
            return;
        }

        // Check all students have a status
        for (int i = 0; i < model.getRowCount(); i++) {

            if (model.getValueAt(i, 1).equals("Pending")) {
                JOptionPane.showMessageDialog(this,
                    "Mark attendance for every student first!");
                return;
            }
        }

        // Current date
        String date = LocalDate.now().format(
            DateTimeFormatter.ofPattern("dd-MM-yyyy")
        );

        // Save each student's attendance
        for (int i = 0; i < model.getRowCount(); i++) {

            String name = model.getValueAt(i, 0).toString();
            String status = model.getValueAt(i, 1).toString();

            int present = (int) model.getValueAt(i, 2);
            int total = (int) model.getValueAt(i, 3);

            total++;

            if (status.equals("Present")) {
                present++;
            }

            double percentage = (present * 100.0) / total;

            // Update attendance summary
            model.setValueAt(present, i, 2);
            model.setValueAt(total, i, 3);

            model.setValueAt(
                String.format("%.2f%%", percentage), i, 4
            );

            // Add date-wise attendance record
            historyModel.addRow(new Object[]{
                date, name, status
            });

            // Reset status
            model.setValueAt("Pending", i, 1);
        }

        JOptionPane.showMessageDialog(this,
            "Attendance saved successfully!");
    }

    // ---------------- BUTTON DESIGN ----------------

    JButton createButton(String text) {

        JButton button = new JButton(text);

        button.setBackground(blue);
        button.setForeground(Color.WHITE);
        button.setFont(new Font("Arial", Font.BOLD, 13));
        button.setFocusPainted(false);

        return button;
    }

    // ---------------- MAIN METHOD ----------------

    public static void main(String[] args) {

        SwingUtilities.invokeLater(() -> {
            new StudentAttendanceSystem().setVisible(true);
        });
    }
}
