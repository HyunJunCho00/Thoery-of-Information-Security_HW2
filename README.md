# Thoery-of-Information-Security_HW2
2024학년도 2학기 정보보호론 과제 2 정리


### Overview of the Padding Oracle Attack

A padding oracle attack is an exploit in block cipher encryption, specifically in CBC (Cipher Block Chaining) mode, that uses padding validation errors to reverse-engineer the plaintext from a ciphertext. In CBC mode, padding is added to the last block during encryption when needed, following a specific scheme. By observing padding error messages, an attacker can extract information about the plaintext. The core of a padding oracle attack is to systematically recover blocks of the plaintext, ultimately reconstructing the entire message by leveraging padding error feedback to gain clues about the underlying plaintext.


### Process of my code

I. IV Initialization and Intermediate Array Setup

In the first line of the code, the initial IV (original_IV) is extracted from C0, represented as a hexadecimal string. Here, C0 is the first block, and this block is used to obtain the Initialization Vector (IV). After this, the IV is initialized as an 8-byte array with all elements set to 0, marking the starting point of the attack. The intermid array is set up to store intermediate values for each byte being recovered. As the attack progresses, this array is gradually filled with the guessed values.

II. Padding Loop

A loop begins to iterate over padding lengths from 1 to 8. Each padding length corresponds to recovering bytes of the plaintext from the last byte to the first, in reverse order.

III. IV Modification and Calculation

In each iteration of the loop, the IV is reset to all 0s. The range_index is set according to the current padding length. For example, when the padding length is 1, range_index is set to 7, aiming to recover this specific byte. A second loop is used to configure each byte in the IV array by XORing the values from intermid with the current padding length. This step is crucial to set up for finding the correct padding.

IV. Byte Guessing and Valid Padding Check

In the third loop, values from 0 to 255 are guessed for the byte at range_index. Each guessed value is set into the modified IV, and the result is combined with C1 to check if the padding is valid. The pad_oracle function uses the modified IV and C1 to verify if the padding is correct. If the padding is valid, the correctly guessed byte value is computed as (guessed_value ^ padding) and stored in the intermid array. This confirms a successful guess for the byte, setting check to True.

Note: If no valid padding is found for a specific range_index, an error message is printed, and the function exits, indicating that the attack has failed.

V. Plaintext Recovery and Output

After repeating the above steps for all padding lengths, the final plaintext is recovered by XORing each byte of original_IV with the corresponding byte in intermid. Finally, the plaintext and original IV are converted to ASCII format and printed for verification. This allows the user to view the recovered plaintext.
