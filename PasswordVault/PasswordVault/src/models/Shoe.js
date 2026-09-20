import mongoose from 'mongoose';

const ShoeSchema = new mongoose.Schema({
  name: { type: String, required: true },
  brand: { type: String },
  price: { type: Number, required: true },
  image: { type: String },
  stock: { type: Number, default: 10 },
});

export default mongoose.models.Shoe || mongoose.model('Shoe', ShoeSchema);